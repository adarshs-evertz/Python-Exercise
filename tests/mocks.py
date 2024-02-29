from typing import Any, Mapping

from db import Db, ItemType
from errors import ItemNotFound


class MockDb(Db):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_item(item_type: ItemType, tenant_id: str, item_id: str, fields=None) -> dict[str, Any]:
        if item_id == "1":
            return {"success": True, "text": "some test text"}
        else:
            raise ItemNotFound(item_type.value, tenant_id, item_id)

    @staticmethod
    def update_item(item_type: ItemType, tenant_id: str, item_id: str, item_data: Mapping[str, Any] = None):
        if item_id == "1":
            return item_data
        else:
            raise ItemNotFound(item_type.value, tenant_id, item_id)

    def delete_item(item_type: ItemType, tenant_id: str, item_id: str, fields=None) -> dict[str, Any]:
        if item_id == "1":
            raise ItemNotFound(item_type.value, tenant_id, item_id)
