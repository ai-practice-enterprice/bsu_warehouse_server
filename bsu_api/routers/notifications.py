from fastapi import APIRouter, File, BackgroundTasks
from typing import Annotated

from utils.emails import send_notification


router = APIRouter(prefix="/notification", tags=["Fake Data"])


@router.post("/robot")
async def read_robot_notification(file: Annotated[bytes, File()], background_tasks: BackgroundTasks):
    """
    Receive information about a robot
    """

    background_tasks.add_task(send_notification, "", file.decode())
    return {"message": "Robot notification received"}
