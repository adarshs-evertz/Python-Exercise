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


# PATCH THE DECORATOR HERE
patch("evertz_io_observability.decorators.start_span", mock_decorator).start()

import handler


class TestHandler:
    @mock.patch("handler.Db")
    def test_get_item_success(self, mock_db, get_correct_item_event):
        event, context = get_correct_item_event

        mock_db.return_value = MockDb()
        response = handler.get_item(event, context)
        assert response["statusCode"] == HTTPStatus.OK
        body = json.loads(response["body"])
        assert body == {"success": True, "text": "some test text"}
        headers = response["headers"]
        assert headers["Content-Type"] == "application/vnd.api+json"

    def test_try_get_item_without_jwt(self, get_item_without_jwt_event):
        event, context = get_item_without_jwt_event
        with pytest.raises(evertz_io_identity_lib.errors.MissingToken):
            handler.get_item(event, context)

    @mock.patch("handler.Db")
    def test_get_item_not_found(self, mock_db, get_not_existing_item_event):
        event, context = get_not_existing_item_event

        mock_db.return_value = MockDb()
        response = handler.get_item(event, context)
        assert response["statusCode"] == HTTPStatus.NOT_FOUND
        body = json.loads(response["body"])
        assert "errors" in body
        assert body["errors"][0]["code"] == "ItemNotFound"

    @mock.patch("service.Service.update_item")
    @mock.patch("handler.Db")
    def test_update_item_success(self, mock_db, mock_service_update_item, update_correct_item_event):
        event, context = update_correct_item_event

        mock_service_update_item.return_value = {
            "id": "some_id",
            "modification_info": {
                "created_at": "2024-02-22T14:42:05.131396",
                "created_by": "4730f174-c00c-4920-982e-e5a4984d9ca4",
                "last_modified_at": "2024-02-22T14:42:05.131396",
                "last_modified_by": "4730f174-c00c-4920-982e-e5a4984d9ca4",
            },
            "text": "test",
            "success": True,
        }
        mock_db.return_value = MockDb()
        response = handler.update_item(event, context)
        assert response["statusCode"] == HTTPStatus.OK
        body = json.loads(response["body"])
        assert body == {"text": "test", "success": True}
        headers = response["headers"]
        assert headers["Content-Type"] == "application/vnd.api+json"

    def test_try_update_item_without_jwt(self, update_item_without_jwt_event):
        event, context = update_item_without_jwt_event
        with pytest.raises(evertz_io_identity_lib.errors.MissingToken):
            handler.update_item(event, context)

    @mock.patch("handler.Db")
    def test_update_item_not_found(self, mock_db, update_not_existing_item_event):
        event, context = update_not_existing_item_event

        mock_db.return_value = MockDb()
        response = handler.update_item(event, context)
        assert response["statusCode"] == HTTPStatus.NOT_FOUND
        body = json.loads(response["body"])
        assert "errors" in body
        assert body["errors"][0]["code"] == "ItemNotFound"

    @mock.patch("handler.Db")
    def test_delete_item_success(self, mock_db, delete_correct_item_event):
        event, context = delete_correct_item_event

        mock_db.return_value = MockDb()
        response = handler.delete_item(event, context)
        assert response["statusCode"] == HTTPStatus.NO_CONTENT

