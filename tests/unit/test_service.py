import json
import uuid
from functools import wraps
from http import HTTPStatus
from unittest.mock import patch

import evertz_io_identity_lib
import mock
import pytest

from tests.mocks import MockDb


def mock_decorator(*args, **kwargs):
    """Decorate by doing nothing."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return decorator


patch("evertz_io_observability.decorators.start_span", mock_decorator).start()

from service import Service


class TestService:
    @mock.patch("service.Db")
    def test_update_item_keys(self, mock_db):
        payload = {"success": True, "text": "some text"}
        tenant_id = "test_tenant"
        user_id = "test_user"
        mock_db.return_value = MockDb()
        new_service = Service(mock_db, tenant_id, user_id)
        item = new_service.create_item(payload)
        item["success"] = False
        updated_item = new_service.update_item(item, item["id"])
        expected_keys = {"id", "modification_info", "success", "text"}
        assert all(key in updated_item for key in expected_keys), "Key not found"
        assert updated_item["id"] == item["id"]
        assert updated_item["success"] == False
