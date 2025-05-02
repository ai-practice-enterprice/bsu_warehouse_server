import logging
from fastapi import APIRouter
from prisma.models import Zones, Robots, Paths, Packages, OrderMovement

router = APIRouter(prefix="/database", tags=["Database"])
log = logging.getLogger(__name__)

@router.get("/live", response_model=dict)
async def get_database_content():
    """
    Get all data from all database tables
    """
    log.info("Fetching all database content")

    try:
        zones = await Zones.prisma().find_many()
        robots = await Robots.prisma().find_many()
        paths = await Paths.prisma().find_many()
        packages = await Packages.prisma().find_many()
        order_movements = await OrderMovement.prisma().find_many()

        return {
            "Zones": zones,
            "Robots": robots,
            "Paths": paths,
            "Packages": packages,
            "OrderMovements": order_movements
        }
    except Exception as e:
        log.error(f"Error collecting data: {e}")
        return {"error": str(e)}
