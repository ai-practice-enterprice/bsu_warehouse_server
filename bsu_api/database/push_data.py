import numpy as np
from utils.qrcodes import generate_qr_code_b64, decode_qr_code_b64
from prisma.models import Robots, Paths, Zones , PackageMovement , Packages , ZoneTypes , RobotTypes
from faker import Faker
from faker.providers import BaseProvider

from datetime import datetime , timedelta
import random
import json 
import csv 
import os

from map_gen.config import (
    MAP ,
    ZONE_TYPE_NAMES ,
    ROWS ,
    COLS ,
    ZONE_TYPE_FOR_ROBOTS ,
    ZONE_TYPE_FOR_ROBOTS_DESC ,
    ZONE_TYPES ,
    ZONE_TYPE_NAMES ,
    ZONE_TYPE_NAMES_DESC ,
    ROBOT_TYPES ,
    ROBOT_NAMES , 
    JETANK ,
    JETRACER ,
    JETANK_HIWONDER ,
    STORAGE
)

from utils.logger import setup_logger
log = setup_logger(__name__)
script_path = os.path.dirname(__file__)

class RobotProvider(BaseProvider):
    ROBOT_TYPES: list = ROBOT_TYPES

    def robotType(self):
        return self.random_element(self.ROBOT_TYPES)
    



class FakeDataGenerator():
    """
    A class for generating and optionally pushing fake data for packages,
    zones, and robots to a database or writing it to JSON files.

    Attributes:
        write_data_to_file (bool): Flag indicating whether to write generated
            data to JSON files. Defaults to True.
        files (dict): A dictionary mapping data types ('packages', 'zones',
            'robots', 'zone_types', 'robot_types') to their corresponding
            JSON file paths.
        package_starting_records (int): The starting number for packages to insert for Day 1.
            Defaults to 100, taken from the 'additional_configuration'.
        package_start_date (datetime): The starting date for generated package timestamps.
            Defaults to January 1, 2020, taken from 'additional_configuration'.
        package_end_date (datetime): The ending date for generated package timestamps.
            Defaults to the current datetime, taken from 'additional_configuration'.
        package_trends (tuple): list of integers describing a trend line (positive or negative)
            Defaults to a tuple of 4 different trends : negative , slighlty negative , slighlty positive , positive  
        robots_number_of_records (int): The number of fake robot records to generate.
            Defaults to 6, taken from 'additional_configuration'.
        only_jetank (bool): If True, only 'jetank' type robots will be generated.
            Defaults to False, taken from 'additional_configuration'.
        only_jetracer (bool): If True, only 'jetracer' type robots will be generated.
            Defaults to False, taken from 'additional_configuration'.
        only_jetank_hiwonder (bool): If True, only 'jetank_hiwonder' type robots
            will be generated. Defaults to False, taken from
            'additional_configuration'.
        zones_map (dict): A dictionary representing the zones map, used for generating
            zone data. Defaults to the global 'MAP' variable, taken from
            'additional_configuration'.
    """
    def __init__(
        self,
        push_packages: bool = True,
        push_zones: bool = True,
        push_robots: bool = True,
        push_paths: bool = True,
        write_to_file: bool = True,
        file_type: str = "json",
        read_from_file: bool = False,
        additional_configuration: dict = {
            "package_starting_records"  : 100,
            "package_start_date"         : datetime(year=2024,month=1,day=1),
            "package_end_date"           : datetime.now(),
            "package_trends"             : (
                [-5, 0, 7, 15, 25, 38, 54],
                [2, 3, 4, 5, 6, 8, 9],
                [-8, -6, -5, -4, -3, -1, 0],
                [-50, -40, -28, -15, 0, 18, 40],
            ),
            "zones_map"                  : MAP,
            "robots_number_of_records"   : 6,
            "only_jetank"                : False,
            "only_jetracer"              : False,
            "only_jetank_hiwonder"       : False,
        },
        files: dict = {
            "packages"      : os.path.join(script_path,"fake_data_packages"),
            "zones"         : os.path.join(script_path,"fake_data_zones"),
            "robots"        : os.path.join(script_path,"fake_data_robots"),
            "zone_types"    : os.path.join(script_path,"fake_data_zone_types"),
            "robot_types"   : os.path.join(script_path,"fake_data_robot_types"),
        }
    ):
        
        self.push_packages = push_packages
        self.push_zones = push_zones
        self.push_robots = push_robots
        self.push_paths = push_paths
        self.push_OM = False
        self.push_PM = False
        self.field_headers = {
            "packages" : [
                "packageID",
                "streetName",
                "houseNumber",
                "cityName",
                "cityPostcode",
                "insertDate",
                "active",
            ],
            "robots" : [
                "robotID",
                "robotStatus",
                "robotType",
                "robotNamespace",
            ],
            "zones" : [
                "zoneID",
                "zoneDescription",
                "zoneName",
                "zoneAvailable",
                "zoneType",
                "zoneX",
                "zoneY",
                "zoneCapacity",
            ],
            "robot_types" : [
                "robotTypeID",
                "robotTypeName",
            ],
            "zone_types" : [
                "zoneTypeID",
                "zoneTypeName",
                "zoneTypeDescription",
            ],
        }

        if self.push_packages and self.push_zones:
            if self.push_robots and self.push_paths:
                self.push_OM = True
            self.push_PM = True

        self.write_data_to_file = write_to_file
        self.read_from_file = read_from_file
        self.files = files
        self.fileType = file_type

        for key , file in self.files.items():
            self.files[key] = file + "." + self.fileType


        self.package_starting_records = additional_configuration.get(
            "package_starting_records",
            100
        )
        self.start_date = additional_configuration.get(
            "package_start_date",
            datetime(
                year=2020,
                month=1,
                day=1,
            )
        )
        self.end_date = additional_configuration.get(
            "package_end_date",
            datetime.now()
        )
        self.package_trends = additional_configuration.get(
            "package_trends",
            (
                [-5, 0, 7, 15, 25, 38, 54],
                [2, 3, 4, 5, 6, 8, 9],
                [-8, -6, -5, -4, -3, -1, 0],
                [-50, -40, -28, -15, 0, 18, 40],
            )
        )
        self.number_of_records = additional_configuration.get(
            "robots_number_of_records",
            6
        )
        self.only_jetank = additional_configuration.get(
            "only_jetank",
            False
        )
        self.only_jetracer = additional_configuration.get(
            "only_jetracer",
            False
        )
        self.only_jetank_hiwonder = additional_configuration.get(
            "only_jetank_hiwonder",
            False
        )
        self.map = additional_configuration.get(
            "zones_map",
            MAP
        )

    async def push(self):
        if self.read_from_file:
            await self.push_data_from_file()
        else:
            if self.push_zones:
                await self.push_fake_zones_to_db()
            if self.push_robots:
                await self.push_fake_robots_to_db()
            if self.push_packages:
                await self.push_fake_packages_to_db()
            if self.push_PM:
                await self.push_fake_PM_to_db()
            if self.push_OM:
                await self.push_fake_OM_to_db()
    # https://www.geeksforgeeks.org/how-to-fix-datetime-datetime-not-json-serializable-in-python/
    def serialize_datetime(self,obj): 
        if isinstance(obj, datetime): 
            return obj.isoformat() 
        raise TypeError("Type not serializable") 
    
    def deserialize_data(self, row:dict):
        for k, v in row.items():
            if k == "streetName" or k == "houseNumber" or k == "cityName" or k == "cityPostcode":
                try:
                    row[k] = str(v)
                    continue
                except (ValueError, TypeError):
                    pass
            else:
                try:
                    row[k] = datetime.fromisoformat(v)
                    continue
                except (ValueError, TypeError):
                    pass

                try:
                    row[k] = int(v)
                    continue
                except (ValueError, TypeError):
                    pass

                try:
                    row[k] = bool(v)
                    continue
                except (ValueError, TypeError):
                    pass

        return row
    
    def write_json(self,filepath: str,data: list[dict]):
        with open(filepath,"w") as f:
            json.dump(data,f,indent=4,default=self.serialize_datetime)
            f.close()

    def write_csv(self,filepath: str,data: list[dict],fieldheaders):
        with open(filepath,"w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldheaders,delimiter=';')
            writer.writeheader()
            writer.writerows(data) 
            f.close()

    # FAKE DATA GENERATOR FUNCTIONS =================================================
    async def push_data_from_file(self):
        for table_db , file_path in self.files.items():
            try:
                with open(file_path,"r") as f:
                    if self.fileType == "json":
                        data = json.load(f,object_hook=self.deserialize_data)
                    elif self.fileType == "csv":
                        reader = csv.DictReader(file_path,delimiter=';')
                        data = []
                        for row in reader:
                            deserialized_row = self.deserialize_data(row)
                            data.append(deserialized_row)
                    else:
                        raise Exception("no valid filetype")
                    if table_db == "packages":      await Packages.prisma().create_many(data=data)
                    if table_db == "zones":         await Zones.prisma().create_many(data=data)
                    if table_db == "robots":        await Robots.prisma().create_many(data=data)
                    if table_db == "zone_types":    await ZoneTypes.prisma().create_many(data=data)
                    if table_db == "robot_types":   await RobotTypes.prisma().create_many(data=data)
            except Exception as e:
                log.info(f"could not read data from file {file_path}: {e.args}")    

    async def push_fake_packages_to_db(self):
        log.info(f"====== Pushing fake packages ======")
        package_data: list = []
        fake = Faker()

        if self.package_starting_records < 0:
            nbr_of_packages = 100
        else:
            nbr_of_packages = self.package_starting_records
        
        # https://www.datacamp.com/tutorial/random-walk
        # https://www.w3schools.com/python/python_datetime.asp
        np_gen = np.random.default_rng(seed=42)
        end_date: datetime = self.end_date
        insert_date: datetime = self.start_date
        packageID = 1
        status_active = False
        current_trend = np_gen.choice(self.package_trends)
        try:
            # ----------------- main loop ----------------- #
            while insert_date <= end_date:
                # fluctuation = int(np_gen.normal(loc=5, scale=15))
                # fluctuation => number of packages to remove or to add to the previous
                # observation (thus this is a markov process), depending on the trend.
                fluctuation = np_gen.choice(current_trend)
                nbr_of_packages += fluctuation

                if np_gen.random() <= 0.05:
                    current_trend = np_gen.choice(self.package_trends)

                if np_gen.random() <= 0.1:
                    eventual_drop = np_gen.choice([-100,-50,-30])
                else :
                    eventual_drop = 0

                if nbr_of_packages < 0:
                    nbr_of_packages = 0

                if insert_date == end_date:
                    status_active = True

                for n in range(nbr_of_packages + eventual_drop):
                    package_data.append({
                        "packageID"    : packageID,
                        "streetName"   : fake.street_name(),
                        "houseNumber"  : str(random.randint(1,300)),
                        "cityName"     : fake.city(),
                        "cityPostcode" : fake.postcode(),        
                        "insertDate"   : insert_date,
                        "active"       : status_active
                    }) 
                    packageID += 1
                insert_date += timedelta(days=1)

        except Exception as e:
            log.info(f"Could not create fake packages record for day {insert_date.strftime('%c')} number of records {nbr_of_packages} {e}")
            
        try:
            await Packages.prisma().create_many(data=package_data)
        except Exception as e:
            log.info(f"Could not insert fake packages into DB {e}")


        if self.write_data_to_file:
            if self.fileType == "json":
                self.write_json(self.files["packages"],package_data)
            elif self.fileType == "csv":
                self.write_csv(self.files["packages"],package_data,self.field_headers["packages"])

            

    async def push_fake_zones_to_db(self):
        log.info(f"====== Pushing fake zones and zone types ======")
        zone_data_types: list = []
        for zone_type in ZONE_TYPES:
            zone_type_name = ZONE_TYPE_NAMES[zone_type]
            zone_tye_desc = ZONE_TYPE_NAMES_DESC[zone_type] 
            zone_data_types.append({
                "zoneTypeID"   : zone_type,
                "zoneTypeName" : zone_type_name,
                "zoneTypeDescription" : zone_tye_desc,
            })
        try:
            await ZoneTypes.prisma().create_many(data=zone_data_types)
        except Exception as e:
            log.info(f"Could not insert fake zone types into DB {e}")

        if self.write_data_to_file:
            if self.fileType == "json":
                self.write_json(self.files["zone_types"],zone_data_types)
            elif self.fileType == "csv":
                self.write_csv(self.files["zone_types"],zone_data_types,self.field_headers["zone_types"])

        zone_data: list = []
        if len(self.map) > 1:
            if len(self.map[0]) == 1:
                log.info("defaulting to standard map...")
                self.map = MAP

        zoneID = 1
        # ----------------- main loop ----------------- #
        for y in range(ROWS):
            for x in range(COLS):
                zone_type = MAP[y][x]
                zone_type_name = ZONE_TYPE_NAMES[zone_type]

                if zone_type in ZONE_TYPE_FOR_ROBOTS_DESC.keys():
                    zone_desc = ZONE_TYPE_FOR_ROBOTS_DESC[zone_type]
                else:
                    zone_desc = ""

                zone_name =  zone_type_name + " " +  str(zoneID)

                zone_data.append({
                    "zoneID"            : zoneID,              
                    "zoneDescription"   : zone_desc,                     
                    "zoneName"          : zone_name,                            
                    "zoneAvailable"     : True,       
                    "zoneType"          : zone_type,            
                    "zoneX"             : x,               
                    "zoneY"             : y,
                    "zoneCapacity"      : 4,               
                })
                zoneID += 1


        try:
            await Zones.prisma().create_many(data=zone_data)
        except Exception as e:
            log.info(f"Could not insert fake zones into DB {e}")

        if self.write_data_to_file:
            if self.fileType == "json":
                self.write_json(self.files["zones"],zone_data)
            elif self.fileType == "csv":
                self.write_csv(self.files["zones"],zone_data,self.field_headers["zones"])

    async def push_fake_robots_to_db(self):
        log.info(f"====== Pushing fake robots ======")

        robot_data_types: list = []
        # ----------------- main loop ----------------- #
        for robot_type in ROBOT_TYPES:
            robot_type_name = ROBOT_NAMES[robot_type]
            
            robot_data_types.append({
                "robotTypeID"   : robot_type,
                "robotTypeName" : robot_type_name,
            })
        try:
            await RobotTypes.prisma().create_many(data=robot_data_types)
        except Exception as e:
            log.info(f"Could not insert fake robot types into DB {e}")

        if self.write_data_to_file:
            if self.fileType == "json":
                self.write_json(self.files["robot_types"],robot_data_types)
            elif self.fileType == "csv":
                self.write_csv(self.files["robot_types"],robot_data_types,self.field_headers["robot_types"])


        robot_data: list = []
        fake = Faker()
        fake.add_provider(RobotProvider)

        if self.only_jetank:
            robot_type_restrication = JETANK
        elif self.only_jetracer:
            robot_type_restrication = JETRACER
        elif self.only_jetank_hiwonder:
            robot_type_restrication = JETANK_HIWONDER
        else:
            robot_type_restrication = "all"


        if self.number_of_records < 0:
            self.number_of_records = 40

        robotID = 1
        # ----------------- main loop ----------------- #
        for x in range(self.number_of_records):
            if robot_type_restrication == "all":
                robot_type = fake.robotType()
            else:
                robot_type = robot_type_restrication

            robot_ns = ROBOT_NAMES[robot_type] + "_" + str(robotID)

            robot_data.append({
                "robotID"        : robotID,
                "robotStatus"    : True,
                "robotType"      : robot_type,
                "robotNamespace" : robot_ns,
            }) 
            robotID += 1
        try:
            await Robots.prisma().create_many(data=robot_data)
        except Exception as e:
            log.info(f"Could not insert fake robots into DB {e}")

        if self.write_data_to_file:
            if self.fileType == "json":
                self.write_json(self.files["robots"],robot_data)
            elif self.fileType == "csv":
                self.write_csv(self.files["robots"],robot_data,self.field_headers["robots"])

    async def push_fake_paths_to_db(self,):
        log.info(f"====== Pushing fake paths ======")
        pass

    # NOTE : PM == PackageMovment
    async def push_fake_PM_to_db(self,):
        log.info(f"====== Pushing fake PMs ======")
        pass

    # NOTE : OM == OrderMovement
    async def push_fake_OM_to_db(self,):
        log.info(f"====== Pushing fake OMs ======")
        pass

    # FAKE DATA GENERATOR FUNCTIONS =================================================