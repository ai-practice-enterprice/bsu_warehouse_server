from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , OrderMovement , ZoneTypes
from fastapi import Depends
import logging
from logging import Logger
import random
from typing import Any , Annotated

from arq import ArqRedis
from arq.jobs import Job
from arq.worker import Retry



# https://arq-docs.helpmanual.io/#retrying-jobs-and-cancellation

# create the taskqueue functions ===========================================================
async def process_order(ctx: dict[Any, Any], zone_id: int, package_id: int):
    log: Logger = ctx["logger"]
    arq_redis: ArqRedis = ctx["arq_redis"]
    log.info(f"Attempting to clear package {package_id} from zone {zone_id}...")

    # 1) Find an available robot
    # 1.1) Exception handeling if no robot available => retry +1
    robots = await Robots.prisma().find_many(
        where={
            "AND" : [
                {
                    "robotStatus" : True
                },
                {
                    "robotAvailable" : True
                }
            ]
        }
    )
    log.info(f"ARQ : Found {len(robots)} free robots.")

    if len(robots) == 0: 
        raise Retry(defer=ctx['job_try'] * 5)
        return "no robot is free"
    else :
        r1 = random.choice(robots)
    log.info(f"Choose robot {r1.robotNamespace} to clear package {package_id}...")
    return "no robot is free"
    
    await Robots.prisma().find_many(
        where={
            "AND" : [
                {
                    "robotStatus" : True
                },
                {
                    "robotAvailable" : True
                }
            ]
        }
    )
    # Lorenzo => 
    # 1.2) Exception handeling if no robot available => retry == max_retries
    
    # 1.2.1) Exception handeling of no robot available => Query DB to verify 
    # 1.2.1.1) Query does not work after 4 query tries ? => Distress call => proceed to full shutdown
    # 1.2.1.2) Confirmation all robots busy ? => Distress call => proceed to normal shutdown

    # full shutdown => all zones are set to False + Error on dashboard should be displayed that DB is down
    # normal shutdown => all zones are set to False

    # 2) from the robots use either manhattan distance as a metric or just random.choices (with or without weights)
    
    # 3) use httpx to send a htttp request using the GET method for the bsu-ros-server (see docker-compose) to handle and then send to the RosApiBridge


async def check_for_package_to_move(ctx: dict[Any, Any]):
    """
    This function is run every X seconds to add jobs to the ARQ (asych redis queue to add a delay)
    => want to change the "X" see the ArqWorker
    """
    log: Logger = ctx["logger"]
    arq_redis: ArqRedis = ctx["arq_redis"]

    try:
        log.info("ARQ : Checking for packages to move")
        new_orders = await PackageMovement.prisma().find_many(
            where={
                'zones': {
                    'zoneTypes': {
                        'zoneTypeName': 'DropZoneIn'
                    }
                }
            },
            include={
                "packages": True,
                "zones" : True,
                "zones": {
                    "include" : {
                        "zoneTypes" : True
                    }
                }, 
            }
        )
        
        log.info(f"ARQ : Found {len(new_orders)} new orders.")
        for pm in new_orders:
            await arq_redis.enqueue_job(
                "process_order",
                zone_id = pm.ZoneID,
                package_id = pm.PackageID
            )

    except Exception as e:
        log.exception(f"ARQ : Error checking for new orders: {e}")

# create the taskqueue functions ===========================================================

