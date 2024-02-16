"""
Manage items.
"""
import datetime
import uuid

from evertz_io_observability.decorators import start_span

from context import logger
from db import Db, ItemType


class Service:
    """Manager Context for Item Actions"""

    def __init__(self, database: Db, tenant_id: str, user_id: str):
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.database = database

    @start_span("service_get_item")
    def get_item(self, item_id: str) -> dict:
        """
        Get an item using a tenant id to scope the lookup

        :param item_id: The id of the user to fetch
        :return: The full info of the item
        """
        logger.info(f"Getting item: {item_id}")
        return self.database.get_item(item_type=ItemType.ITEM, tenant_id=self.tenant_id, item_id=item_id)

    @start_span("service_create_item")
    def create_item(self, item: dict) -> dict:
        """
        Create item

        :param item: the item data to be saved

        :return: Dict
        """
        logger.info(f"Creating Item: {item}")
        now = datetime.datetime.utcnow().isoformat()
        item["modification_info"] = {
            "created_at": now,
            "created_by": self.user_id,
            "last_modified_at": now,
            "last_modified_by": self.user_id,
        }

        item["id"] = str(uuid.uuid4())
        try:
            self.database.put_item(
                item_type=ItemType.ITEM, tenant_id=self.tenant_id, item_id=item["id"], item_data=item
            )
        except Exception as error:
            print(error)
            # tests errors here
            raise error
        return item
