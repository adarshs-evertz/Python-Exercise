import json
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
    def test_update_item(self, mock_db,):
        
        item = {"success": True, "text":"some text"}
        tenant_id = 'test_tenant'
        user_id = 'test_user'
        new_service = Service(mock_db.return_value, tenant_id, user_id)
        item_id = new_service.create_item(item)
        new_item = {"success": False, "text":"some text"}
        response = new_service.update_item(item, item_id)
        expected_dict={"id", "modification_info", "success","text"}
        assert all(key in response for key in expected_dict), "Key not found"
        assert response["id"] == item["id"]
        modification = item["modification_info"]
        assert response["modification_info"]["created_at"] == modification["created_at"]
        assert response["modification_info"]["created_by"] == modification["created_by"]
        

