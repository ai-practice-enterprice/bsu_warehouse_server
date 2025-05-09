import os
import random

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from prisma.models import Zones , PackageMovement , Packages , OrderMovement , ZoneTypes
from typing import Annotated
from faker import Faker

from map_gen.MapPlotter import MapPlotter 
from map_gen.config import TILE_SIZE , ZONE_TYPE_FOR_ROBOTS , ZONE_TYPE_FOR_ROBOTS_DESC

from utils.logger import setup_logger
log = setup_logger(__name__)
router = APIRouter(prefix="/frontend", tags=["Frontend"])

# ======================== API fake AD team DATABASE ======================== #

# THIS IS A TEMP FUNC SO CHANGES ARE ALLOWED TO INCREASE REALASTIC BEHAVIOUR (such as: DB conn failed , courrier missing , no data fetched , etc...)
def fetch_fake_remote_packagedata_from_AD_team(courrier_id: int,courrier_max_id: int = 20):

    # 1% chance of error
    if random.randint(1,1000) == 1:
        raise Exception("Could not connect...")

    # courier does not exist
    if courrier_id not in range(1,courrier_max_id + 1):
        raise Exception("Courrier does not exist...")

    # other errors that you might think of that could break our server
    # ...
    #  ...

    data: list[dict] = []
    fake = Faker()
    for x in range(courrier_id*10,courrier_id*10 + 10):
        data.append({
            "packageID"    : x,
            "courrierID"   : random.randint(1,courrier_max_id),
            "streetName"   : fake.street_name(),
            "houseNumber"  : str(random.randint(1,300)),
            "cityName"     : fake.city(),
            "cityPostcode" : fake.postcode(),            
        }) 

    fetched_data: list[dict] = []
    for package in data:
        if package["courrierID"] == courrier_id: 
            fetched_data.append(package)
    
    return fetched_data

# ======================== models for API request (NOT for database => see schema.prisma) ======================== #

class ZoneCreationRequest(BaseModel):
    zone_name: str = Field(alias="zoneName")
    zone_type: str = Field(alias="zoneType")
    zone_description: str = Field(alias="zoneDescription")
    zone_available: bool = Field(alias="zoneAvailable")
    zone_check: bool = Field(alias="zoneCheck")

# ======================== API endpoints for zone data ======================== #
@router.get("/zone/all")
async def read_zones():
    """
    Fetch all zones
    """
    zones = await Zones.prisma().find_many(include={"zoneTypes":True})
    return zones

@router.get("/zone/type/all")
async def read_zone_types():
    """
    Fetch all zone types
    """
    zoneTypes = await ZoneTypes.prisma().find_many()
    return zoneTypes

@router.get("/zone/type", response_model=list[Zones])
async def read_zones_of_type(
    zone_type: Annotated[str, Query()] = ZONE_TYPE_FOR_ROBOTS[0]
):
    """
    Fetch all zone of certain type (e.g.: RobotStation , DropZoneIn , ErrorZone)
    """
    if zone_type not in ZONE_TYPE_FOR_ROBOTS:
        return []
    
    zone_type_record = await ZoneTypes.prisma().find_first(
        where={"zoneTypeName": zone_type}
    )
    
    if zone_type_record.zoneTypeID is None:
        return []

    zones = await Zones.prisma().find_many(
        where={"zoneType": zone_type_record.zoneTypeID},
        include={"zoneTypes":True},
        order={"zoneID":"asc"},
    )
    return zones

@router.patch("/zone/data/{zone_id}")
async def read_single_zone(
    zone_id: int
):
    """
    Fetch data of 1 zone
    """
    zone = await Zones.prisma().find_unique(
        where={"zoneID" : zone_id},
        include={"zoneTypes":True}
    )
    return zone

@router.post("/zone/map_warehouse",responses={200 : {"content": {"image/xml+svg": {}},}})
async def get_map_warehouse():
    """
    Fetch the warehouses interactive map base upon MapPlotter
    """

    zones = await Zones.prisma().find_many(include={"zoneTypes" : True})

    path_to_map = os.path.join(
        os.path.dirname(__file__),
        "..",
        "map_gen",
        "map.svg"
    )

    mp = MapPlotter(
        data=zones,
        mode="SVG",
        tilesize=TILE_SIZE,
        filename=path_to_map,
        border=False,
    )
    mp.draw_edges()
    mp.draw_nodes(radius=5)
    mp.save_map()

    return FileResponse(path=path_to_map)


@router.post("/zone")
async def create_zone(zone: ZoneCreationRequest):
    """
    Create a new zone
    """
    log.info(f"Creating a new zone: {zone.zone_name} of type {zone.zone_type}")
    await Zones.prisma().create({
        "zoneName": zone.zone_name,
        "zoneType": zone.zone_type,
        "zoneDescription": zone.zone_description,
        "zoneAvailable": zone.zone_available,
        "zoneCheck": zone.zone_check
    })
    return {"status": "success"}


@router.patch("/zone/{zone_id}/toggle")
async def toggle_zone_availability(zone_id: int):
    """
    Toggle the availability of a zone
    """
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")

    new_availability = not zone.zoneAvailable
    await Zones.prisma().update(where={"zoneID": zone_id}, data={"zoneAvailable": new_availability})

    return {"status": "succes"}

@router.get("/zone/change/capacity")
async def change_zone_capacity(zone_id: int,new_zone_capacity: int):
    """
    change the capacity of a zone
    """
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    await Zones.prisma().update(
        where={"zoneID": zone_id}, 
        data={                   
            "zoneCapacity" : new_zone_capacity,                            
        }
    )

    return {"status" : "success"}

@router.get("/zone/type/count")
async def get_zone_type_count():
    """
    fetch the zone count per type
    """
    zone_counts = await Zones.prisma().group_by(
        by=["zoneType"],
        count=True,
    )

    zone_types = await ZoneTypes.prisma().find_many()
    zone_type_name_map = {zt.zoneTypeID: zt.zoneTypeName for zt in zone_types}

    formatted_data = []
    for count_item in zone_counts:
        zone_type_id = count_item["zoneType"]
        count = count_item["_count"]["_all"]
        zone_type_name = zone_type_name_map.get(zone_type_id)
        if zone_type_name:
            formatted_data.append({"zoneTypeName": zone_type_name, "count": count})

    return formatted_data

@router.get("/zone/change/type")
async def change_zone_type(zone_id: int,new_zone_type: str):
    """
    change the type of a zone
    """
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    zone_type = await ZoneTypes.prisma().find_first(where={"zoneTypeName":new_zone_type})
    if not zone_type:
        raise HTTPException(status_code=404, detail="Zone type not found")
    if zone_type.zoneTypeID in ZONE_TYPE_FOR_ROBOTS_DESC.keys():
        zone_desc = ZONE_TYPE_FOR_ROBOTS_DESC[zone_type.zoneTypeID]
    else:
        zone_desc = ""

    zone_name =  new_zone_type + " " +  str(zone_id)
    await Zones.prisma().update(
        where={"zoneID": zone_id}, 
        data={
            "zoneType": zone_type.zoneTypeID,
            "zoneDescription"   : zone_desc,                     
            "zoneName"          : zone_name,                            
        }
    )

    return {"status" : "success"}

@router.patch("/zone/{zone_id}/enter")
async def enter_zone(zone_id: int,courrier_id: int = 1):
    """
    Mark a zone as entered
    """
    # early fails to prevent the worker from entering a unavailable zone
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        log.exception(f"Zone {zone_id} not found")
        raise HTTPException(status_code=404, detail="Zone not found")
    if not zone.zoneAvailable:
        log.exception(f"Zone {zone_id} not available")
        raise HTTPException(status_code=400, detail="Zone is not available")
    
    # --- !!! NEEDS TO BE REPLACED WITH ACTUAL URL and COURRIER ID !!! --- #
    try:
        # REAL
        # packages_fetched = httpx.get(url=f"http://bsu-ad-server/courriers?courrierID={courrier_id}")

        # FAKE
        courrier_id = random.randint(1,20)
        packages_fetched = fetch_fake_remote_packagedata_from_AD_team(courrier_id)

    except Exception as e:
        log.exception(f"AD Server unresponsive. Please try again later... \n arguments => {e.args}")
        raise HTTPException(status_code=500, detail="AD Server unresponsive")
    
    # --- !!! NEEDS TO BE REPLACED WITH ACTUAL URL and COURRIER ID !!! --- #

    # 1) here we create the data (might not be necessary but we might also get back some fields that we don't require)
    # that is tailored for our dataabase
    insert_data_package = []
    insert_data_packageMov = []
    for package in packages_fetched:
        insert_data_package.append({
            "packageID" : package["packageID"],
            "streetName" : package["streetName"], 
            "houseNumber" : package["houseNumber"], 
            "cityName" : package["cityName"], 
            "cityPostcode" : package["cityPostcode"], 
        })

        insert_data_packageMov.append({
            "ZoneID" : zone_id,
            "PackageID" : package["packageID"],
        })
    try:
        # 2) here we add the packages to the DB
        await Packages.prisma().create_many(
            data=insert_data_package
        )
        # 3) here we add the packages about WHERE they are inside the warehouse (hopefully) to the DB
        await PackageMovement.prisma().create_many(
            data=insert_data_packageMov
        )
    except Exception as e:
        log.exception(f"AI Server encountered some error when trying to insert the fetched data {e}")
        raise HTTPException(status_code=500, detail="AI Server encountered some error when trying to insert the fetched data")
    try:
        # 4) here we update the zone
        await Zones.prisma().update(where={"zoneID": zone_id}, data={"zoneAvailable": False})
    except Exception as e:
        log.exception(f"AI Server encountered some error when trying to update the zone {e}")
        raise HTTPException(status_code=500, detail="AI Server encountered some error when trying to update the zone")
    # 5) finally we need to return something to the user 
    # so that the warehouse worker and courrier can move on 
    # the job for ARQ to handle will be created later on because of the cron job we have running
    return {"succes" : "Packages have registered"}


@router.patch("/zone/{zone_id}/exit")
async def exit_zone(zone_id: int):
    """
    Mark a zone as exited
    """
    zone = await Zones.prisma().find_unique(where={"zoneID": zone_id})
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    if zone.zoneAvailable:
        raise HTTPException(status_code=400, detail="Zone is already available")

    await Zones.prisma().update(where={"zoneID": zone_id}, data={"zoneAvailable": True})

    return {"status": "success"}






