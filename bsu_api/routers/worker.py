import logging
from fastapi import APIRouter


router = APIRouter(prefix="/workers", tags=["Worker Data"])
log = logging.getLogger(__name__)


@router.get("/arrival", response_model=str)
def worker_arrival_confirmation(worker_id: int,zone_id: int):
    """
    Confirms that the driver has arrived at the warehouse and assigns an available load-out zone.
    In this example, load-out zones in the database are marked with 'zoneType' equal to "loadOut"
    and are considered available if 'zoneAvailable' is True.
    """
    log.info(f"sending response to worker (arriving at warehouse)")

    return str(f"Okay Worker arrived at zone {zone_id}")
    

@router.get("/departure",response_model=str)
def get_worker_departure_confirmation(worker_id: int, zone_id: int):
    """
    Get a Okay response from the server, when departing
    """
    log.info(f"sending response to worker (leaving from warehouse)")

    return str(f"Okay Worker departed from zone {zone_id}")
