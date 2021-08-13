from uuid import UUID

from api.tests.unit.utils import BaseModelTest
from api.tests.unit.test_schemas_chapter import TestChapterSchema

import api.schemas.upload as sch


class TestBeginUploadSession(BaseModelTest):
    schema = sch.BeginUploadSession
    example_data = {
        "manga_id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"),
        "chapter_id": UUID("116bdaa6-f62d-4b53-98b2-237adbaad788"),
    }
    correct_data = [
        {
            "manga_id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"),
            "chapter_id": None,
        }
    ]
    wrong_data = [
        # Missing fields
        {
            "chapter_id": UUID("116bdaa6-f62d-4b53-98b2-237adbaad788"),
        }
    ]
    irregular_data = [
        # String to uuid
        {
            "manga_id": "1e01d7f6-c4e1-4102-9dd0-a6fccc065978",
            "chapter_id": UUID("116bdaa6-f62d-4b53-98b2-237adbaad788"),
        },
        {
            "manga_id": UUID("1e01d7f6-c4e1-4102-9dd0-a6fccc065978"),
            "chapter_id": "116bdaa6-f62d-4b53-98b2-237adbaad788",
        },
    ]


class TestUploadedBlobResponse(BaseModelTest):
    schema = sch.UploadedBlobResponse
    example_data = {
        "id": UUID("eadec6fe-619f-4d7f-8328-f8a5563d3325"),
        "name": "001.png",
    }
    wrong_data = [
        # Missing fields
        {
            "name": "001.png",
        },
        {
            "id": UUID("eadec6fe-619f-4d7f-8328-f8a5563d3325"),
        },
    ]
    irregular_data = [
        # String to uuid
        {
            "id": "eadec6fe-619f-4d7f-8328-f8a5563d3325",
            "name": "001.png",
        }
    ]


class TestUploadSessionResponse(BaseModelTest):
    schema = sch.UploadSessionResponse
    parent = TestBeginUploadSession
    example_data = {
        **parent.example_data,
        "id": UUID("6970baa2-4932-497d-a3e0-4b5545252dc6"),
        "blobs": [],
    }
    correct_data = [
        {
            "id": UUID("6970baa2-4932-497d-a3e0-4b5545252dc6"),
            "blobs": [TestUploadedBlobResponse.example_data],
        },
    ]
    wrong_data = [
        # Missing fields
        {
            "blobs": [TestUploadedBlobResponse.example_data],
        },
    ]
    irregular_data = [
        # String to uuid
        {
            "id": "6970baa2-4932-497d-a3e0-4b5545252dc6",
            "blobs": [],
        },
        # Default values
        {
            "id": UUID("6970baa2-4932-497d-a3e0-4b5545252dc6"),
        },
    ]


class TestCommitUploadSession(BaseModelTest):
    schema = sch.CommitUploadSession
    example_data = {
        "chapter_draft": TestChapterSchema.example_data,
        "page_order": [UUID("eadec6fe-619f-4d7f-8328-f8a5563d3325")],
    }
    wrong_data = [
        # Missing fields
        {
            "page_order": [UUID("eadec6fe-619f-4d7f-8328-f8a5563d3325")],
        },
        {
            "chapter_draft": TestChapterSchema.example_data,
        },
    ]
    irregular_data = [
        # String to uuid
        {
            "chapter_draft": TestChapterSchema.example_data,
            "page_order": ["eadec6fe-619f-4d7f-8328-f8a5563d3325"],
        },
    ]
