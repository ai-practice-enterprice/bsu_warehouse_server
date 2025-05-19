# this are a few implementations of ARQ but mostly besed upon
# => https://safir.lsst.io/user-guide/arq.html
# => https://arq-docs.helpmanual.io/#simple-usage
import logging
import json
import httpx
import zenoh
import asyncio
from arq import cron, create_pool, ArqRedis
from prisma import Prisma 
from typing import Any

from .worker_functions import check_for_package_to_move, process_order, receive_robot_notification, notify_zone_map
from config import ARQ_REDIS_SETTINGS
from utils.logger import setup_logger

# ======================== ARQ coroutines to run at certain events ======================== #
# ctx == context is dictionary that will be passed around that the worker requires
# it is the 1st variable in any function executed by a ARQ worker 
async def startup(ctx: dict[str, Any]):
    """Runs during worker start-up to set up the worker context."""
    ctx["logger"] = setup_logger(__name__)

    ctx["logger"].info("------------ Worker start up running ------------")
    # The instance key uniquely identifies this worker in logs
    async_http_client = httpx.AsyncClient()
    ctx["http_client"] = async_http_client
    # because the ARQ worker runs in a separate process and doesn't share the same 
    # Prisma instance or async context as our FastAPI app, we need to create a new Prisma instance
    prisma_query_engine = Prisma(auto_register=True)
    await prisma_query_engine.connect()
    ctx["prisma"] = prisma_query_engine

    ctx["zenoh"] = zenoh.open(zenoh.Config.from_json5(json.dumps({
        "mode": "peer",
        "connect": {
            "endpoints": ["tcp/192.168.1.10:7447"]
            # "endpoints": ["tcp/192.168.65.3:7447"]
        }
    })))
    ctx["zenoh_pub"] = ctx["zenoh"].declare_publisher("**/goal_position")
    ctx["zenoh_pub_robot_reset"] = ctx["zenoh"].declare_publisher("server/**/reset")
    ctx["zenoh_pub_zone"] = ctx["zenoh"].declare_publisher("server/map")
    ctx["zenoh_rec_task"] = asyncio.create_task(asyncio.to_thread(receive_robot_notification, ctx["zenoh"], ctx["logger"]))

    # arq == asyn Redis queue 
    # => arq is the same as python's rq library but it uses asynchio on top of it
    ctx["arq_redis"] = await create_pool(ARQ_REDIS_SETTINGS)

    ctx["logger"].info("------------ Worker start up complete ------------")

    startup.ctx = ctx

async def shutdown(ctx: dict[Any, Any]):
    """Runs during worker shutdown to cleanup resources."""
    log: logging.Logger = ctx["logger"]
    async_http_client: httpx.AsyncClient = ctx["http_client"]
    prisma_query_engine: Prisma = ctx["prisma"]
    arq_redis: ArqRedis = ctx["arq_redis"]
    zenoh_client: zenoh.Session = ctx["zenoh"]
    pub_task: asyncio.Task = ctx["zenoh_rec_task"]

    try:
        pub_task.cancel()
        await pub_task
        log.info("Zenoh task cancelled")

    except asyncio.CancelledError:
        log.info("Zenoh receive cancelled task => cancelled error")

    log.info("------------ Worker shutdown running ------------")
    try:
        await async_http_client.aclose()
        log.info("closing the http_client")

    except Exception as e:
        log.warning("Issue closing the http_client : %s", str(e))

    try:
        await prisma_query_engine.disconnect()
        log.info("closing the prisma query engine")

    except Exception as e:
        log.warning("Issue closing the prisma query engine : %s", str(e))

    try:
        await arq_redis.close()
        log.info("closing the ArqRedis instance")
    
    except Exception as e:
        log.warning("Issue closing the ArqRedis instance : %s", str(e))

    try:
        zenoh_client.close()
        log.warning("closing the zenoh client")

    except Exception as e:
        log.warning("Issue closing the zenoh client : %s", str(e))

    log.info("------------ Worker shutdown complete ------------")


# ======================== ARQ worker settings ======================== #
# see https://arq-docs.helpmanual.io/#arq.worker.Worker for details on these attributes
class WorkerSettings:
    """
    Configuration for the arq worker
    """
    functions = [process_order]
    on_startup = startup
    on_shutdown = shutdown

    redis_settings = ARQ_REDIS_SETTINGS

    # Set retry settings for jobs
    max_tries = 3
    retry_jobs = True
    
    # override context for jobs
    ctx = dict()
    ctx["job_try"] = 1  # Starting job try count
    ctx["max_tries"] = max_tries  # Explicitly set the max tries for the job

    # https://arq-docs.helpmanual.io/#cron-jobs
    cron_jobs = [
        # not sure if we should put a max tries on this one since we try every X seconds anyway
        # but if a bigger interval is required maybe then, we can keep it at as is or increase it even 
        cron(
           coroutine=check_for_package_to_move,
           name="check packages to move regulary",
           second=20,
           max_tries=2
        ),
        cron(
            coroutine=notify_zone_map,
            name="notify zone map",
            second=20,
            max_tries=2
        )
    ]
