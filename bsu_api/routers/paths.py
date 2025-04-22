from fastapi import APIRouter, HTTPException 
from pydantic import BaseModel, Field
from prisma.models import Paths
from typing import List
from utils.logger import setup_logger
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])


# ======================== models for API request (NOT for database => see schema.prisma) ======================== #

class PathCreationRequest(BaseModel):
    path_number: int = Field(alias="pathNumber")
    path_description: str = Field(alias="pathDescription")
    path_zone_start: int = Field(alias="pathZoneStart")
    path_zone_end: int = Field(alias="pathZoneEnd")
    path_coordinates: List[List[float]] = Field(alias="pathCoordinates")
    path_active: bool = Field(alias="pathActive")



# ======================== API endpoints for path data ======================== #
@router.get("/path/all")
async def read_paths():
    """
    Fetch all paths with zone information
    """
    paths = await Paths.prisma().find_many(
        include={
            "zoneStart": True,
            "zoneEnd": True
        }
    )
    return paths


@router.post("/path")
async def create_path(path: PathCreationRequest):
    """
    Create a new path
    """
    log.info(f"Creating a new path: {path.path_number} from zone {path.path_zone_start} to {path.path_zone_end}")
    
    # Convert the coordinates to a string for storage
    path_coordinates_str = str(path.path_coordinates)
    
    await Paths.prisma().create({
        "pathNumber": path.path_number,
        "pathDescription": path.path_description,
        "pathZoneStart": path.path_zone_start,
        "pathZoneEnd": path.path_zone_end,
        "pathCoordinates": path_coordinates_str,
        "pathActive": path.path_active
    })
    
    return {"status": "success"}


@router.patch("/path/{path_id}/toggle")
async def toggle_path_status(path_id: int):
    """
    Toggle the active status of a path
    """
    path = await Paths.prisma().find_unique(where={"pathID": path_id})
    if not path:
        raise HTTPException(status_code=404, detail="Path not found")

    new_status = not path.pathActive
    await Paths.prisma().update(where={"pathID": path_id}, data={"pathActive": new_status})

    return {"status": "success"}