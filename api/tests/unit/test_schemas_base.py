from api.tests.unit.utils import BaseModelTest

from api.config import get_settings
import api.schemas.base as sch

settings = get_settings()


class TestPaginationResponse(BaseModelTest):
    schema = sch.PaginationResponse
    example_data = {
        "offset": 2,
        "limit": settings.max_page_limit,
        "results": [],
        "total": 10,
    }
    wrong_data = [
        # Missing fields
        {
            "limit": settings.max_page_limit,
            "results": [],
            "total": 10,
        },
        {
            "offset": 2,
            "results": [],
            "total": 10,
        },
        {
            "offset": 2,
            "limit": settings.max_page_limit,
            "total": 10,
        },
        {
            "offset": 2,
            "limit": settings.max_page_limit,
            "results": [],
        },
        # Field limits
        {
            "offset": -1,
            "limit": settings.max_page_limit,
            "results": [],
            "total": 10,
        },
        {
            "offset": 2,
            "limit": 0,
            "results": [],
            "total": 10,
        },
        {
            "offset": 2,
            "limit": settings.max_page_limit + 1,
            "results": [],
            "total": 10,
        },
        {
            "offset": 2,
            "limit": settings.max_page_limit,
            "results": [],
            "total": -1,
        },
    ]
    irregular_data = [
        # String to number
        {
            "offset": 2,
            "limit": str(settings.max_page_limit),
            "results": [],
            "total": 10,
        },
        {
            "offset": "2",
            "limit": settings.max_page_limit,
            "results": [],
            "total": 10,
        },
        {
            "offset": 2,
            "limit": settings.max_page_limit,
            "results": [],
            "total": "10",
        },
    ]
