import random
import zenoh
from typing import Any
import httpx
import asyncio
from logging import Logger
from prisma.models import Robots, Zones , PackageMovement, OrderMovement
from arq import ArqRedis
from arq.worker import Retry


# https://arq-docs.helpmanual.io/#retrying-jobs-and-cancellation
# create the taskqueue functions ===========================================================
async def process_order(ctx: dict[str, Any], zone_id: int, package_id: int, coords: tuple[int, int]):
    log: Logger = ctx["logger"]
    http_client: httpx.AsyncClient = ctx["http_client"]
    zenoh_pub: zenoh.Publisher = ctx["zenoh_pub"]
    log.info(f"Attempting to clear package {package_id} from zone {zone_id}...")

    # 1) Find an available robot or retry if no robot available
    try:
        robots = await Robots.prisma().find_many(
            where={"AND": [
                {"robotStatus" : True}, {"robotAvailable" : True}
            ]}
        )
        log.info(f"ARQ : Found {len(robots)} free robots.")

        # 1.2) Exception handling if no robot available => retry == max_retries
        if len(robots) == 0:
            raise Retry(defer=ctx['job_try'] * 5)
            # if ctx['job_try'] < ctx['max_tries']: # If we're not at the max retries yet, retry with a delay
            #     log.info(f"No robots available, retry {ctx['job_try']}/{ctx['max_tries']}")
            #     raise Retry(defer=ctx['job_try'] * 5)
            # else:
            #     # We've reached max retries, verify if all robots are truly busy
            #     log.info("Max retries reached. Verifying robot availability in the database...")
                
            #     # 1.2.1) Exception handling of no robot available => Query DB to verify
            #     query_attempts = 0
            #     max_query_attempts = 4  # Max number of query attempts
                
            #     while query_attempts < max_query_attempts:
            #         try:
            #             query_attempts += 1
            #             count_result = await Robots.prisma().count(where={
            #                 "robotStatus": True
            #             })
                        
            #             robots_busy_count = await Robots.prisma().count(
            #                 where={
            #                     "AND": [
            #                         {"robotStatus": True},
            #                         {"robotAvailable": False}
            #                     ]
            #                 }
            #             )
                        
            #             # Check if query response is OK
            #             if count_result == robots_busy_count and count_result > 0:
            #                 # All robots are busy - Query response OK but all robots busy
            #                 log.warning("Distress call: All robots are busy!")
                            
            #                 # Send distress call
            #                 await send_distress_call(http_client, log, "All robots are busy", is_full_shutdown=False)
                            
            #                 # Normal shutdown - set all zones to unavailable
            #                 await normal_shutdown(log)
            #                 return "distress call sent - all robots busy"
                        
            #             # Some robots should be available soon
            #             log.info(f"Robots status: {robots_busy_count} busy out of {count_result} total robots")
            #             # Retry one more time with a longer delay
            #             raise Retry(defer=30)
                        
            #         except Exception as e:
            #             log.error(f"Database query attempt {query_attempts} failed: {str(e)}")
            #             if query_attempts >= max_query_attempts:
            #                 # 1.2.1.1) Query does not work after 4 query tries => Distress call => full shutdown
            #                 log.critical("Distress call: Database connectivity issues!")
                            
            #                 # Send distress call
            #                 await send_distress_call(http_client, log, "Database connectivity issues", is_full_shutdown=True)
                            
            #                 # Full shutdown - set all zones to unavailable and flag DB as down
            #                 await full_shutdown(log)
            #                 return "distress call sent - database issues"
        
        # If we have robots available, randomly select one
        r1 = random.choice(robots)
        log.info(f"Choose robot {r1.robotNamespace} to clear package {package_id}...")
        
        # 2) With the robot selected, mark it as unavailable
        updated_robot = await Robots.prisma().update_many(
            where={"robotID": r1.robotID, "robotAvailable": True},
            data={"robotAvailable": False}
        )
        if updated_robot == 0:
            log.error(f"Failed to mark robot {r1.robotNamespace} as unavailable")
            raise Retry(defer=5)
        log.info(f"Robot {r1.robotNamespace} marked as unavailable")
        
        # 2.1) Create an OrderMovement entry to track this task
        try:
            # Create order movement to associate the robot with this task
            order = await OrderMovement.prisma().create(
                data={
                    "RobotID": r1.robotID,
                    "ZoneID": zone_id,
                    "status": "processing"
                }
            )
            log.info(f"Created order {order.OrderID} for package {package_id} with robot {r1.robotNamespace}")
        except Exception as e:
            log.error(f"Failed to create order movement: {str(e)}")
            # Revert robot availability since we failed to create the order
            await Robots.prisma().update(
                where={"robotID": r1.robotID},
                data={"robotAvailable": True}
            )
            raise Retry(defer=5)
        
        # 3) Send Zenoh pub to tell robot to move
        try:
            await asyncio.to_thread(zenoh_pub.put, "")
        except Exception as e:
            log.error(f"Error sending request to RosApiBridge: {str(e)}")
            # Revert robot availability
            await Robots.prisma().update(
                where={"robotID": r1.robotID},
                data={"robotAvailable": True}
            )
            # Update order status to failed
            await OrderMovement.prisma().update(
                where={"OrderID": order.OrderID},
                data={"status": "failed"}
            )
            return "error sending request to robot"
        
    except Exception as e:
        log.error(f"Error processing order: {str(e)}")
        return f"error processing order: {str(e)}"


async def check_for_package_to_move(ctx: dict[Any, Any]):
    """
    This function is run every X seconds to add jobs to the ARQ (asych redis queue to add a delay)
    => want to change the "X" see the ArqWorker
    """
    log: Logger = ctx["logger"]
    arq_redis: ArqRedis = ctx["arq_redis"]

    try:
        log.info("ARQ : Checking for packages to move")
        # Find packages in DropZoneIn zones that don't already have an active order
        new_orders = await PackageMovement.prisma().find_many(
            where={
                "zones": {
                    "is": {"zoneTypes": {
                        "is": {"zoneTypeName": "DropZoneIn"}
                    }}
                }
            },
            include={
                "packages": True,
                "zones": {
                    "include": {
                        "zoneTypes": True
                    }
                }
            }
        )
        
        log.info(f"ARQ : Found {len(new_orders)} new orders.")
        for pm in new_orders:
            # Check if there's already an active order for this package
            existing_orders = await OrderMovement.prisma().count(
                where={
                    "ZoneID": pm.ZoneID,
                    "status": {"in": ["pending", "processing"]}
                }
            )
            
            if existing_orders == 0:
                await arq_redis.enqueue_job(
                    "process_order",
                    zone_id=pm.ZoneID,
                    package_id=pm.PackageID,
                    coords=(pm.zones.zoneX, pm.zones.zoneY)
                )
    except Exception as e:
        log.exception(f"ARQ : Error checking for new orders: {e}")

# create the taskqueue functions ===========================================================
