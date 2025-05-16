import pkgutil
import importlib
from datetime import datetime

import zenoh.zenoh
import routers
from typing import AsyncIterator
from dotenv import load_dotenv

from contextlib import asynccontextmanager

from prisma import Prisma

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# contains all URL configurations 
from config import ORIGINS , ARQ_REDIS_SETTINGS

# contains all functions to generate fake DB
from database.push_data import FakeDataGenerator

from map_gen.config import MAP

from utils.logger import setup_logger

import zenoh

# loads env variables (can be implemented or said later on to increase security (such as passwords and other env variables))
load_dotenv(override=True)

log = setup_logger(__name__)
zenoh_session = None

# FastAPI (https://realpython.com/fastapi-python-web-apis/)
# uses events or a lifespan parameter to handle it's runtime logic before booting and after shutdown
# however you must choose between the 2. as stated in the docs "It's all lifespan or all events, not both."
# https://fastapi.tiangolo.com/advanced/events/#async-context-manager  
@asynccontextmanager
async def lifespan(_) -> AsyncIterator[None]:
    log.info("Starting up")

    # Prisma requires a client. The client is a auto-generated and type-safe query builder that's tailored to your data. (as stated in the docs : https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/introduction)
    # the Prisma client requires a schema file (usually : schema.prisma) which is a file that defines: 
    # - the "models" (tables in your DB) , 
    # - your datasource (your URL where your DB is located)
    # - and your generator (which is your DB provider) 
    # Once the prisma file is made and Prisma is INSTALLED you  can run "prisma generate" in the root of the directory 
    # You can also run "prisma studio" which offers a GUI to the database for developement
    log.info("Starting up : connecting with Prisma query engine...")
    prisma = Prisma(auto_register=True)
    await prisma.connect()

    # add fake data to DB =====================================================
    log.info("Starting up : pushing fake data to DB...")
    fake_date_gen = FakeDataGenerator(
        push_packages = False,
        push_zones = True,
        push_robots = False,
        push_robot_types = True,
        push_paths = False,
        push_users = True, 
        write_to_file = False,
        read_from_file = False,
        file_type = "csv",
        additional_configuration = {
            "package_starting_records"  : 80,
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
        }
    )
    await fake_date_gen.push()
    # add fake data to DB =====================================================
    
    yield
    log.info("Shutting down")
    log.info("Shutting down : Prisma query engine")
    await prisma.disconnect()

# Create main app ===================================================== 
app = FastAPI(lifespan=lifespan)

# add the CORS for allowing other application to talk to the API server
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    # instead of all (*) for security use => ORIGINS from the config file
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Create main app ===================================================== 


# add routers =====================================================
# Register all submodules of the router module i.e. all routers inside the routers folder
for module_info in pkgutil.iter_modules(routers.__path__):
    module = importlib.import_module(f'routers.{module_info.name}')
    if hasattr(module, "router"):
        log.info(f"Registering routes from {module_info.name}")
        app.include_router(module.router)
# add routers =====================================================
