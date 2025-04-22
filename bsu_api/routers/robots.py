from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from prisma.models import Robots, RobotTypes
from utils.logger import setup_logger
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])


# ======================== models for API request (NOT for database => see schema.prisma) ======================== #

class RobotCreationRequest(BaseModel):
    robot_type: str = Field(alias="robotType")
    robot_namespace: str = Field(alias="robotNamespace")
    robot_status: bool = Field(alias="robotStatus")



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
            "robotType": robot_type_id,
            "robotStatus": robot.robot_status
        },
        include={"RobotTypes":True}
    )

    return new_robot


@router.get("/robot/all")
async def read_robots():
    """
    Fetch all robots
    """
    robots = await Robots.prisma().find_many(include={"RobotTypes":True})
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
        include={"RobotTypes":True}
    )

    return updated_robot
