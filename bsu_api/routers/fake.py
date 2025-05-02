import logging
import random
from enum import Enum
from datetime import datetime, timedelta
from fastapi import APIRouter, Query
from typing import Annotated
from faker import Faker
from faker.config import AVAILABLE_LOCALES
from faker_airtravel import AirTravelProvider 

# available fake models ==========================================================================
# based upon the AD team's ERD 
from models import (
    Customer,
    Package,
    Airline,
    Airplane,
    Airport,
    City,
    Flight,
    Location,
)

router = APIRouter(prefix="/fake", tags=["Fake Data"])
AvailableLocales = Enum("AvailableLocales", {loc: loc for loc in AVAILABLE_LOCALES})
log = logging.getLogger(__name__)


@router.get("/customers", response_model=list[Customer])
def get_fake_customer_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for customers for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake customers with locale {locale}")

    return [
        Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
        )
        for _ in range(limit)
    ]


@router.get("/packages", response_model=list[Package])
def get_fake_parcel_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for packages for testing purposes based on the provided limit and locale
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake packages with locale {locale}")

    return [
        Package(
            reference="".join(fake.random_letters(32)),
            dimension=f"{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}x{fake.random_int(min=1, max=100)}",
            status=random.choice(["pending", "in_transit", "delivered"]),
            name=fake.first_name(),
            lastname=fake.last_name(),
            receiverEmail=fake.email(),
            receiver_phone_number=fake.phone_number(),
        )
        for _ in range(limit)
    ]


@router.get("/locations", response_model=list[Location])
def get_fake_locations_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake locations with locale {locale}")

    LocationNames = Enum("pickup point", "distribution center", "airport")

    return [
        Location(
            name=fake.company(),
            location_type=fake.enum(LocationNames).name,
            contact_number=fake.phone_number(),
            opening_hours=f"{fake.random_int(min=6,max=12)} AM - {fake.random_int(min=1,max=9)} PM"
        )
        for _ in range(limit)
    ]


@router.get("/flights", response_model=list[Flight])
def get_fake_flights_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake flights with locale {locale}")

    StatusFlight = Enum("departed", "arrived", "underway")

    fake_flight_data: list[Flight] = []

    for _ in range(limit):
        today = datetime.today()
        departure_date = fake.date_this_year()
        status_current_flight = fake.enum(StatusFlight)

        if status_current_flight.name == "departed":
            arrival_date = fake.date_between_dates(
                date_start=today,
                date_end=departure_date + timedelta(days=fake.random_int(0,3))
            )
        elif status_current_flight.name == "arrived":
            arrival_date = fake.date_between_dates(
                date_start=departure_date,
                date_end=today
            )
        elif status_current_flight.name == "underway":
            arrival_date = departure_date + timedelta(
                days=fake.random_int(0,3),
                hours=(abs(random.random()) % 24)
            )
        
        
        fake_flight_data.append(
            Flight(
                departure_time=datetime.combine(departure_date, datetime.min.time()),
                arrival_time=datetime.combine(arrival_date, datetime.min.time()),
                status=status_current_flight.name,
            )
        )

    return fake_flight_data


@router.get("/cities", response_model=list[City])
def get_fake_cities_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale.value)

    log.info(f"Generating {limit} fake cities with locale {locale}")

    return [
        City(
            name=fake.city(),
            postcode=fake.postcode()
        )
        for _ in range(limit)
    ]


@router.get("/airplanes", response_model=list[Airplane])
def get_fake_airplanes_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale=locale.value)
    fake.add_provider(AirTravelProvider)
    

    log.info(f"Generating {limit} fake airplanes with locale {locale}")

    return [
        Airplane(
            model=fake.airport_object()["iata"],
            capacity=fake.random_int(15,600),
            status="",
        )
        for _ in range(limit)
    ]


@router.get("/airports", response_model=list[Airport])
def get_fake_airports_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale=locale.value)
    fake.add_provider(AirTravelProvider)

    log.info(f"Generating {limit} fake airports with locale {locale}")

    return [
        Airport(name=fake.airport_name())
        for _ in range(limit)
    ]


@router.get("/airlines", response_model=list[Airline])
def get_fake_airlines_data(
    limit: Annotated[int, Query(ge=1, le=100)] = 1,
    locale: Annotated[AvailableLocales, Query()] = AvailableLocales.nl_BE,  # type: ignore
):
    """
    Get fake data for testing purposes based on the provided limit and locale.
    """

    fake = Faker(locale=locale.value) 
    fake.add_provider(AirTravelProvider)

    log.info(f"Generating {limit} fake airlines with locale {locale}")

    return [
        Airline(
            name=fake.airport_name(),
            IATA_code=fake.airport_iata(),
            contact_number=fake.phone_number(),
            headquarters_location=fake.city(),
        )
        for _ in range(limit)
    ]
