# this are a few implementations of ARQ but mostly besed upon
# => https://safir.lsst.io/user-guide/arq.html
# => https://arq-docs.helpmanual.io/#simple-usage
from arq import cron , create_pool , ArqRedis
from arq.connections import RedisSettings
from .worker_functions import check_for_package_to_move, process_order
from config import ARQ_REDIS_SETTINGS

from prisma import Prisma 

from fastapi import HTTPException

from typing import Any
from httpx import AsyncClient

from logging import Logger 
from utils.logger import setup_logger


# ======================== ARQ coroutines to run at certain events ======================== #
# ctx == context is dictionary that will be passed around that the worker requires
# it is the 1st variable in any function executed by a ARQ worker 
async def startup(ctx: dict[Any, Any]):
    """Runs during worker start-up to set up the worker context."""
    ctx["logger"] = setup_logger(__name__)

    ctx["logger"].info("------------ Worker start up running ------------")
    # The instance key uniquely identifies this worker in logs
    async_http_client = AsyncClient()
    ctx["http_client"] = async_http_client
    # because the ARQ worker runs in a separate process and doesn’t share the same 
    # Prisma instance or async context as our FastAPI app, we need to create a new Prisma instance
    prisma_query_engine = Prisma(auto_register=True)
    await prisma_query_engine.connect()
    ctx["prisma"] = prisma_query_engine

    # arq == asyn Redis queue 
    # => arq is the same as python's rq library but it uses asynchio on top of it
    ctx["arq_redis"] = await create_pool(ARQ_REDIS_SETTINGS)

    ctx["logger"].info("------------ Worker start up complete ------------")

async def shutdown(ctx: dict[Any, Any]):
    """Runs during worker shutdown to cleanup resources."""
    log: Logger = ctx["logger"]
    async_http_client: AsyncClient = ctx["http_client"]
    prisma_query_engine: Prisma = ctx["prisma"]
    arq_redis: ArqRedis = ctx["arq_redis"]

    log.info("------------ Worker shutdown running ------------")
    try:
        await async_http_client.aclose()
    except Exception as e:
        log.warning("Issue closing the http_client : %s", str(e))

    try:
        await prisma_query_engine.disconnect()
    except Exception as e:
        log.warning("Issue closing the prisma query engine : %s", str(e))

    try:
        await arq_redis.close()
    except Exception as e:
        log.warning("Issue closing the ArqRedis instance : %s", str(e))

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

    ctx = dict()
    ctx["job_try"] = 5
    max_tries = 3
    retry_jobs = True

    # https://arq-docs.helpmanual.io/#cron-jobs
    cron_jobs = [
        # not sure if we should put a max tries on this one since we try every X seconds anyway
        # but if a bigger interval is required maybe then, we can keep it at as is or increase it even 
        cron(
           coroutine=check_for_package_to_move,
           name="check packages to move regulary",
           second=20,
           max_tries=2
        )
    ]
