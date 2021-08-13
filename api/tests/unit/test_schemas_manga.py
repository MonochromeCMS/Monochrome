from datetime import datetime
from uuid import UUID

from api.tests.unit.utils import BaseModelTest
from api.tests.unit.test_schemas_base import TestPaginationResponse

from api.models.manga import Status
import api.schemas.manga as sch


class TestMangaSchema(BaseModelTest):
    schema = sch.MangaSchema
    example_data = {
        "title": "Monochrome Lovers",
        "description": "One day, suddenly, an angel came descending from the sky!?",
        "author": "Hibiki Mio",
        "artist": "Hibiki Mio",
        "year": 2021,
        "status": Status.ongoing,
    }
    correct_data = [
        {
            "title": "Monochrome Lovers",
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "author": "Hibiki Mio",
            "artist": "Hibiki Mio",
            "year": None,
            "status": Status.ongoing,
        }
    ]
    wrong_data = [
        # Missing fields
        {
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "author": "Hibiki Mio",
            "artist": "Hibiki Mio",
            "year": 2021,
            "status": Status.ongoing,
        },
        {
            "title": "Monochrome Lovers",
            "author": "Hibiki Mio",
            "artist": "Hibiki Mio",
            "year": 2021,
            "status": Status.ongoing,
        },
        {
            "title": "Monochrome Lovers",
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "artist": "Hibiki Mio",
            "year": 2021,
            "status": Status.ongoing,
        },
        {
            "title": "Monochrome Lovers",
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "author": "Hibiki Mio",
            "year": 2021,
            "status": Status.ongoing,
        },
        {
            "title": "Monochrome Lovers",
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "author": "Hibiki Mio",
            "artist": "Hibiki Mio",
            "year": 2021,
        },
    ]
    irregular_data = [
        # String to number
        {
            "title": "Monochrome Lovers",
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "author": "Hibiki Mio",
            "artist": "Hibiki Mio",
            "year": "2021",
            "status": Status.ongoing,
        },
        # String to enum
        {
            "title": "Monochrome Lovers",
            "description": "One day, suddenly, an angel came descending from the sky!?",
            "author": "Hibiki Mio",
            "artist": "Hibiki Mio",
            "year": 2021,
            "status": "ongoing",
        },
    ]


class TestMangaResponse(BaseModelTest):
    schema = sch.MangaResponse
    parent = TestMangaSchema
    example_data = {
        **parent.example_data,
        "version": 2,
        "id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"),
        "create_time": datetime(2000, 8, 24),
    }
    wrong_data = [
        # Missing fields
        {"id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"), "create_time": datetime(2000, 8, 24)},
        {"version": 2, "create_time": datetime(2000, 8, 24)},
        {
            "version": 2,
            "id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"),
        },
    ]
    irregular_data = [
        # String to number
        {"version": "2", "id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"), "create_time": datetime(2000, 8, 24)},
        # String to UUID
        {"version": 2, "id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978", "create_time": datetime(2000, 8, 24)},
        # String to datetime
        {"version": 2, "id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978", "create_time": "2000-08-24 00:00:00"},
    ]


class TestMangaSearchResponse(BaseModelTest):
    schema = sch.MangaSearchResponse
    parent = TestPaginationResponse
    example_data = {**parent.example_data, "results": [TestMangaResponse.example_data]}
