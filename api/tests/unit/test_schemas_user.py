from uuid import UUID

from api.tests.unit.utils import BaseModelTest
from api.tests.unit.test_schemas_base import TestPaginationResponse

import api.schemas.user as sch


class TestTokenResponse(BaseModelTest):
    schema = sch.TokenResponse
    example_data = {
        "access_token": "ThisIsAToken",
        "token_type": "bearer",
    }
    wrong_data = [
        # Missing fields
        {
            "token_type": "bearer",
        },
        # Constant
        {
            "access_token": "ThisIsAToken",
            "token_type": "NotBearer",
        },
    ]
    irregular_data = [
        # Default values
        {
            "access_token": "ThisIsAToken",
        }
    ]


class TestUser(BaseModelTest):
    schema = sch.User
    example_data = {
        "username": "user",
        "email": "user@example.com",
    }
    correct_data = [
        {
            "username": "user",
            "email": None,
        }
    ]
    wrong_data = [
        # Missing fields
        {
            "email": "user@example.com",
        },
        # Max username length
        {
            "username": "userAbove15Characters",
            "email": "user@example.com",
        },
        # Bad email
        {
            "username": "user",
            "email": "NotAnEm@il",
        },
    ]


class TestUserSchema(BaseModelTest):
    schema = sch.UserSchema
    parent = TestUser
    example_data = {
        **parent.example_data,
        "password": "password",
    }
    wrong_data = [
        # Missing fields
        {}
    ]


class TestUserResponse(BaseModelTest):
    schema = sch.UserResponse
    parent = TestUser
    example_data = {
        **parent.example_data,
        "id": UUID("6901d7f6-c4e1-4200-9dd0-a6fccc065978"),
    }
    wrong_data = [
        # Missing fields
        {},
    ]
    irregular_data = [
        # String to uuid
        {
            "id": "6901d7f6-c4e1-4200-9dd0-a6fccc065978",
        }
    ]


class TestUsersResponse(BaseModelTest):
    schema = sch.UsersResponse
    parent = TestPaginationResponse
    example_data = {**parent.example_data, "results": [TestUserResponse.example_data]}
