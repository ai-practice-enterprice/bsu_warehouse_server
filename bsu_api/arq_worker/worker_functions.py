import random
import zenoh
import time
from typing import Any
import httpx
import json
import asyncio
import requests
import json
from logging import Logger
from prisma.models import Robots, Zones , PackageMovement, OrderMovement
from arq import ArqRedis
from arq.worker import Retry
from .emailTemplates import JinjaEmailTemplateBuilder , MessageType
from pycdr import cdr

# !!!!! This classes should match the ROS2 messages send by the robots
@cdr
class String:
    data: str


# https://arq-docs.helpmanual.io/#retrying-jobs-and-cancellation
# create the taskqueue functions ===========================================================
async def process_order(ctx: dict[str, Any], zone_id: int, package_id: int, coords: tuple[int, int], final_coords: tuple[int, int]):
    log: Logger = ctx["logger"]
    zenoh_pub: zenoh.Publisher = ctx["zenoh_pub"]
    log.info(f"\t ARQ : Attempting to clear package {package_id} from zone {zone_id}...")

    # 1) Find an available robot or retry if no robot available
    try:
        robots = await Robots.prisma().find_many(
            where={"AND": [
                {"robotStatus" : True}, {"robotAvailable" : True}
            ]}
        )
        log.info(f"\t ARQ : Found {len(robots)} free robots.")

        # 1.2) Exception handling if no robot available => retry == max_retries
        if len(robots) == 0:
            raise Retry(defer=ctx['job_try'] * 5)
        
        # If we have robots available, randomly select one
        r1 = random.choice(robots)
        log.info(f"\t ARQ : Choose robot {r1.robotNamespace} to clear package {package_id}...")
        
        # 2) With the robot selected, mark it as unavailable
        updated_robot = await Robots.prisma().update_many(
            where={"robotID": r1.robotID, "robotAvailable": True},
            data={"robotAvailable": False}
        )
        if updated_robot == 0:
            log.error(f"\t ARQ : Failed to mark robot {r1.robotNamespace} as unavailable")
            raise Retry(defer=5)
        log.info(f"\t ARQ : Robot {r1.robotNamespace} marked as unavailable")
        
        # 2.1) Create an OrderMovement entry to track this task
        try:
            # Create order movement to associate the robot with this task
            order = await OrderMovement.prisma().create(
                data={
                    "RobotID": r1.robotID,
                    "ZoneID": zone_id,
                    "PackageID": package_id,
                    "status": "processing"
                }
            )
            log.info(f"\t ARQ : Created order {order.OrderID} for package {package_id} with robot {r1.robotNamespace}")
        except Exception as e:
            log.error(f"\t ARQ : Failed to create order movement: {str(e)}")
            # Revert robot availability since we failed to create the order
            await Robots.prisma().update(
                where={"robotID": r1.robotID},
                data={"robotAvailable": True}
            )
            raise Retry(defer=5)
        
        # 3) Send Zenoh pub to tell robot to move
        try:
            payload = String(
                json.dumps({
                    "robot_namespace": "/" + r1.robotNamespace, 
                    "package_id": package_id, 
                    "x": coords[0], 
                    "y": coords[1],
                    "final_x": final_coords[0],
                    "final_y": final_coords[1],
                })
            ).serialize()
            await asyncio.to_thread(zenoh_pub.put, payload)
        except Exception as e:
            log.error(f"\t ARQ : Error sending request to robot: {str(e)}")
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
        log.error(f"\t ARQ : Error processing order: {str(e)}")
        return f"error processing order: {str(e)}"


## CRON TASKS ===========================================================

async def notify_zone_map(ctx: dict):
    """
    Send the new zone map to the robots
    """
    log: Logger = ctx["logger"]
    zenoh_pub_zone: zenoh.Publisher = ctx["zenoh_pub_zone"]
    
    log.info(f"\t ARQ : Trying to gather map from DB")
    zones = await Zones.prisma().find_many(include={"zoneTypes":True})
    zones_list = []
    for zone in zones:
        zones_list.append({
            "coords": (zone.zoneX, zone.zoneY),
            "zone_id": zone.zoneTypes.zoneTypeID,
        })

    data = String(json.dumps(zones_list)).serialize()
    try:
        await asyncio.to_thread(zenoh_pub_zone.put, data)
        log.info(f"\t ARQ : Sending new zone map to robots")
    except Exception as e:
        log.error(f"\t ARQ : Error sending zone map to robots: {str(e)}")
        return f"error sending zone map to robots: {str(e)}"


async def check_for_package_to_move(ctx: dict):
    """
    This function is run every X seconds to add jobs to the ARQ (asych redis queue to add a delay)
    => want to change the "X" see the ArqWorker
    """
    log: Logger = ctx["logger"]
    arq_redis: ArqRedis = ctx["arq_redis"]

    try:
        log.info("\t ARQ : Checking for packages to move")
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

        storage_zones = await Zones.prisma().find_many(
            where={"zoneTypes": {
                "is": {"zoneTypeID": 3}
            }},
            include={"zoneTypes": True}
        )
        log.info(f"\t ARQ : Found {len(storage_zones)} storage zones.")
        
        log.info(f"\t ARQ : Found {len(new_orders)} new orders.")
        # Check if there's already an active order for package
        for pm in new_orders:
            existing_orders = await OrderMovement.prisma().count(
                where={
                    "PackageID": pm.PackageID,
                    "status": {"in": ["pending", "processing"]}
                }
            )
            
            random_zone = random.choice(storage_zones)
            
            if existing_orders == 0:
                await arq_redis.enqueue_job(
                    "process_order",
                    zone_id=pm.ZoneID,
                    package_id=pm.PackageID,
                    coords=(pm.zones.zoneX, pm.zones.zoneY),
                    final_coords=(random_zone.zoneX, random_zone.zoneY)
                )
    except Exception as e:
        log.exception(f"\t ARQ : Error checking for new orders: {e}")

# create the taskqueue functions ===========================================================


def receive_robot_notification(zenoh_client: zenoh.Session, log: Logger):
    """
    This function handles the notification from the robot
    """
    def send_email(builder: JinjaEmailTemplateBuilder, message: dict): 
        builder.build_email(
            robot_namespace = message["robot_namespace"],
            robot_message = message["robot_message"]
        )

        url = 'http://192.168.1.20:8000/sendmailhtml'
        # url = 'http://192.168.1.20:8000/sendmail'
        headers = {
            'Content-Type': 'application/json',
        }

        # "SSS@blueskyunlimited.org","AD@blueskyunlimited.org"
        # sends a email to the mail server
        for destination in ["AI@blueskyunlimited.org"]: 
            data = {
                "token"         : "knhqwYD2gwJm2zEmXgbrDh",
                "destination"   : destination,
                "subject"       : "test-api",
                "content"       : builder.render(),
            }

            json_data = json.dumps(data)
            response = requests.post(url, data=json_data,headers=headers)

            log.info(f"{response.status_code}")
            if response.status_code != 200:
                log.info(f"{response.json()}")

    def send_notification(builder: JinjaEmailTemplateBuilder, message: dict):
        # sends a notification to the frontend
        builder.build_frontend_notification(
            robot_namespace = message["robot_namespace"],
            robot_message = message["robot_message"]
        )
        requests.post(
            url="http://localhost:8000/notification/all",
            json={"message": builder.render()}
        )

    # ---------------------------------------------------- #
    def callback(sample: zenoh.Sample):

        # https://zenoh.io/blog/2021-04-28-ros2-integration/
        notification: String =  String.deserialize(sample.payload.to_bytes())

        log.info(f"\t ARQ : Payload received: {notification.data.strip("~")}")
        
        try:
            message = json.loads(notification.data.strip("~"))
            # here we should handle the namespace so we know which robot sent the message
            # sample.key_expr => full topic name e.g.: /jetank_1/to_server
            log.info(
                f"""
                \t ARQ :
                \nReceived message from robot: {sample.key_expr}
                \nFull Message: 
                \n\t robot namespace : {message["robot_namespace"]}
                \n\t message type    : {message["message_type"].upper()}
                \n\t robot message   : {message["robot_message"]}
                """
            )

            namespace = message["robot_namespace"][1:] if message["robot_namespace"][0] == "/" else message["robot_namespace"]
            message_type = MessageType.INFO

            if message["message_type"].upper() == "INFO": message_type = MessageType.INFO
            elif message["message_type"].upper() == "WARNING": message_type = MessageType.WARNING
            elif message["message_type"].upper() == "REQUEST": message_type = MessageType.REQUEST
            elif message["message_type"].upper() == "CONFIRMATION": message_type = MessageType.CONFIRMATION
            else: message_type = MessageType.INFO



            if message_type == MessageType.CONFIRMATION:
                package_id = message["package_id"]
                status = message["status"]
                status = message["status"]
                log.info(f"""
                    Requesting Updating robot: {namespace}
                    \n\t status : {status}
                """)
                requests.patch(url=f"http://localhost:8000/frontend/package/{package_id}/done")
                requests.patch(url=f"http://localhost:8000/frontend/robot/namespace/{namespace}/toggle",params={"status" : status})

            elif message_type == MessageType.REQUEST:
                status = message["status"]
                log.info(f"""
                    Requesting Updating robot: {namespace}
                    \n\t status : {status}
                """)
                requests.patch(url=f"http://localhost:8000/frontend/namespace/robot/namespace/{namespace}/toggle",params={"status" : status})

            elif message_type == MessageType.WARNING:
                pass
            elif message_type == MessageType.INFO:
                pass
            else:
                pass
        
            builder = JinjaEmailTemplateBuilder(message_type)
            send_notification(builder, message)
            send_email(builder,message)

        except requests.exceptions.RequestException as e:
            log.warning(f"\t ARQ : An error occurred during the request: {e}")
        except json.JSONDecodeError as e:
            log.warning(f"\t ARQ : Failed to parse JSON payload: {e}")
        except Exception as e:
            log.warning(f"\t ARQ : Unknown error occured {e}")
    # ---------------------------------------------------- #
    


    subscriber = zenoh_client.declare_subscriber("**/to_server", callback)
    log.info("Zenoh subscriber declared for robot notifications")

    while True:
        try:
            time.sleep(1)
        except:
            break
