import datetime
import unittest

from tests.poster_mock import free_port, start_server
from timeless.companies.models import Company
from timeless.employees.models import Employee
from timeless.poster.api import Poster, Authenticated
from timeless.sync.sync import PosterSync
from timeless.restaurants.models import Location


class TestSync(unittest.TestCase):

    locations = [
        {
            "id":40,
            "name":"Pao Pao Cafe",
            "code":"P",
            "company_id":50,
            "country":"United States",
            "region":"Nay",
            "city":"South",
            "address":"Delta Park, 145",
            "longitude":640,
            "latitude":480,
            "type":"L",
            "status":"open",
            "comment":"Brazilian cafe"
        },
        {
            "id":150,
            "name":"Central Perk",
            "code":"C",
            "company_id":50,
            "country":"United States",
            "region":"Manhattan",
            "city":"New York",
            "address":"5th Avenue 145",
            "longitude":1024,
            "latitude":720,
            "type":"C",
            "status":"open",
            "comment":"Cafe from famous sitcom"
        },

    ]

    @classmethod
    def setup_class(cls):
        cls.port = free_port()
        start_server(cls.port, locations=cls.locations)
        cls.company = Company(
            name="Any company",
            code="Cpny",
            employees=[
                Employee(username="rmyers", password="rm1",
                         first_name="Richard", last_name="Myers",
                         phone_number="112233",
                         birth_date=datetime.datetime.utcnow(), pin_code=4567,
                         email="test@test.com"
                         )
            ],
            locations=[
                Location(
                    id=40,
                    name="Tapper",
                    code="T",
                    company_id=50,
                    poster_id=2,
                    synchronized_on=datetime.datetime(1983, 5, 10)
                ),
                Location(
                    id=150,
                    name="Hard Rock",
                    code="H",
                    company_id=50,
                    poster_id=10,
                    synchronized_on=datetime.datetime(1983, 5, 10)
                )
            ])
        auth_poster = Authenticated()
        cls.poster_sync = PosterSync
        cls.poster = Poster(
            url="http://localhost:{port}".format(port=cls.port)
        )


    def test_sync_location(self):
        self.poster_sync.sync_location(self.poster, self.company)
        for location in self.company.locations:
            for poster_location in self.poster.locations():
                if location.id == poster_location["id"]:
                    assert (
                        location.id == poster_location["id"] and
                        location.name == poster_location["name"] and
                        location.code == poster_location["code"] and
                        location.company_id == poster_location["company_id"] and
                        location.country == poster_location["country"] and
                        location.region == poster_location["region"] and
                        location.city == poster_location["city"] and
                        location.address == poster_location["address"] and
                        location.longitude == poster_location["longitude"] and
                        location.latitude == poster_location["latitude"] and
                        location.type == poster_location["type"] and
                        location.status == poster_location["status"] and
                        location.comment == poster_location["comment"]
                    )

