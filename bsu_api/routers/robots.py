import asyncio
from fastapi import APIRouter, HTTPException , Request
from pydantic import BaseModel, Field
from prisma.models import Robots, RobotTypes
from utils.logger import setup_logger
from arq_worker.worker_functions import String
import json
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])


# ======================== models for API request (NOT for database => see schema.prisma) ======================== #

class RobotCreationRequest(BaseModel):
    robot_type: str = Field(alias="robotType")
    robot_namespace: str = Field(alias="robotNamespace")
    robot_status: bool = Field(alias="robotStatus")

class RobotStatusUpdate(BaseModel):
    status: bool


# ======================== API endpoints for robot data ======================== #
@router.post("/robot")
async def create_robot(robot: RobotCreationRequest):
    """
    Create a new robot
    """
    log.info(f"Creating a new robot: {robot.robot_namespace} of type {robot.robot_type}")

    robot_type_id = await RobotTypes.prisma().find_first(where={"robotTypeName" : robot.robot_type})

    if not robot_type_id:
        raise HTTPException(status_code=404, detail="Robot type not found")

    new_robot = await Robots.prisma().create(
        data={
            "robotNamespace": robot.robot_namespace,
            "robotType": robot_type_id.robotTypeID,
            "robotStatus": robot.robot_status
        },
        include={"robotTypes":True}
    )

    return new_robot


@router.get("/robot/all")
async def read_robots():
    """
    Fetch all robots
    """
    robots = await Robots.prisma().find_many(include={"robotTypes":True})
    return robots


@router.get("/robot/type/all")
async def read_robot_types():
    """
    Fetch all robot types
    """
    robot_types = await RobotTypes.prisma().find_many()
    return robot_types


@router.patch("/robot/{robot_id}/toggle")
async def update_robot(robot_id: int):
    """
    Update the status of a robot
    """
    robot = await Robots.prisma().find_unique(where={"robotID": robot_id})
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    else:
        new_status = not robot.robotStatus

    updated_robot = await Robots.prisma().update(
        where={"robotID": robot_id}, 
        data={"robotStatus": new_status},
        include={"robotTypes":True}
    )

    return updated_robot


@router.patch("/robot/{robot_id}/reset")
async def reset_robot(robot_id: int, request: Request):
    """
    Reset a robot to its initial state
    """
    robot = await Robots.prisma().find_unique(where={"robotID": robot_id})
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    
    updated_robot = await Robots.prisma().update(
        where={"robotID": robot_id},
        data={"robotStatus": True, "robotAvailable": True},
    )

    payload = String(
        json.dumps({
            "robot_namespace": "/" + updated_robot.robotNamespace,
            "reset" : True,
            # these could of course be changed via the frontend 
            "direction": False,
            "start_position": False,
            "current_position": False,
            "state": False,
        })
    ).serialize()

    log.info(f"Sending to robot: {payload}")

    await asyncio.to_thread(request.app.state.zenoh_reset_publisher.put,payload)

    log.info(f"Robot {robot_id} has been reset")
    return updated_robot


@router.patch("/robot/namespace/{namespace}/toggle")
async def update_robot_by_namespace(namespace: str, status: bool):
    """
    Update a robot by its namespace
    """
    log.info(f"Updating robot: {namespace}")

    robot_id = await Robots.prisma().find_first(where={"robotNamespace": namespace})

    if not robot_id:
        raise HTTPException(status_code=404, detail="Robot not found")

    updated_robot = await Robots.prisma().update(
        where={"robotID": robot_id.robotID},
        data={
            "robotAvailable": status
        }
    )

    return updated_robot
