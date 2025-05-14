import logging
import random
from fastapi import APIRouter, Query

# API endpoints for camera live feed (viewed on the webserver) data ==========================================================================

# NOT YET IMPLEMENTED BECAUSE NOT REQUIRED

router = APIRouter(prefix="/camera", tags=["Camera Data"])
log = logging.getLogger(__name__)

@router.get("/zonein")
def get_zone_camera_feed_zonein():
    """
    Get camera feed from the RP 
    """
    log.info(f"fetching camera feed data from RP(rasberry pi)")

    return [
        str("...waiting on connection")
    ]

@router.get("/zoneout")
def get_zone_camera_feed_zoneout():
    """
    Get camera feed from the RP 
    """
    log.info(f"fetching camera feed data from RP(rasberry pi)")

    return [
        str("...waiting on connection")
    ]