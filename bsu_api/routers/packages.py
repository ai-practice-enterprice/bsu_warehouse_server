from fastapi import APIRouter, HTTPException , Query
from map_gen.config import STORAGE
from prisma.models import Packages , PackageMovement
from typing import Annotated
from utils.logger import setup_logger
from datetime import datetime
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])

# ==================Annotated====== API endpoints for package data ======================== #
@router.get("/package/all")
async def read_package_grouped_by(
    group_by: Annotated[str , Query(enum=["day","month"])] = "day"
):
    """
    Fetch all packages based upon a date range
    """
    try:
        if group_by == "day":
            time_gap = group_by
        elif group_by == "month": 
            # how to ???
            time_gap = group_by
        else:
            raise Exception(f"no group by {group_by} possible")
    except Exception as e:
        log.info(e.args)
    
    packages = await Packages.prisma().group_by(
        by=["insertDate"],
        count=True
    )

    return [{"date": row["insertDate"], "count": row["_count"]["_all"]} for row in packages]

@router.get("/package/date")
async def read_package_for_date(
    day: Annotated[int , Query()] = None,
    month: Annotated[int , Query()] = None,
    year: Annotated[int , Query()] = None,
):
    """
    Fetch all packages for a specific date
    """

    if not day and not month and not year:
        raise HTTPException(status_code=400,detail="No date was given")
        
    packages = await Packages.prisma().find_many(
        where={
            "insertDate":datetime(
                year=year,
                month=month,
                day=day
            )
        }
    )

    if not packages:
        raise HTTPException(status_code=400,detail="No packages found for date")

    return [{"date": row["insertDate"], "count": row["_count"]["_all"]} for row in packages]

@router.post("/packagemovement/all")
async def read_package_movement_all():
    """
    Fetch all packagemovement
    """
    pm = await PackageMovement.prisma().find_many()
    return pm 

@router.post("/packagemovement/storage")
async def read_package_movement_storage():
    """
    Fetch storage data from packagemovement
    """
    pm = await PackageMovement.prisma().group_by(
        by=["insertDate","zoneTypeID"],
        count=True,
        where={"zoneTypeID":STORAGE}
    )
    return [{"date": row["insertDate"], "count": row["_count"]["_all"]} for row in pm]


