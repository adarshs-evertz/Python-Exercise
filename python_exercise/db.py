"""
The module contains functionality to work with DynamoDB.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Optional

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from evertz_io_dynamo_utils.expressions import projection_expression, update_expression
from evertz_io_identity_lib.iam import restricted_table
from evertz_io_observability.decorators import start_span

from config import TABLE_NAME
from context import logger
from errors import ItemConflict, ItemNotFound

# String used as the delimiter for separating information in the overloaded keys
KEY_DELIMITER = "#"

# Names of keys used in database
PK_KEY = "pk"
DATA_ATTRIBUTE = "data"
ITEM_ID_ATTRIBUTE = "item_id"


class ItemType(Enum):
    """
    Class describes possible types of the primary objects stored in DynamoDB table
    """

    ITEM = "item"


def _get_db_key(item_type: ItemType, tenant_id: str, item_id: Optional[str] = None) -> str:
    """
    Build key that consists of tenant name, item type, and optional item id
    :param item_type: type of the item referenced by key
    :param tenant_id: tenant name
    :param item_id: id of the item referenced by the key
    :return: string representing the key
    """
    if item_id:
        return f"{tenant_id}{KEY_DELIMITER}{item_type.value}{KEY_DELIMITER}{item_id}"

    return f"{tenant_id}{KEY_DELIMITER}{item_type.value}"


@dataclass(frozen=True)
class ItemKeys:
    """
    Class representing keys used to access single primary item
    """

    primary: str
    global_secondary: str

    @staticmethod
    @start_span()
    def get_keys(item_type: ItemType, tenant_id: str, item_id: str) -> "ItemKeys":
        """
        Generate ItemKeys from given parameters
        :param item_type: type of the item referenced by key
        :param tenant_id: tenant name
        :param item_id: id of the item referenced by the key
        :return: new object representing keys for the item
        """
        return ItemKeys(
            primary=_get_db_key(item_type, tenant_id, item_id), global_secondary=_get_db_key(item_type, tenant_id)
        )


class Db:
    """
    The class contains functionality to work with DynamoDB.
    """

    @staticmethod
    @start_span("database_put_item")
    def put_item(item_type: ItemType, tenant_id: str, item_id: str, item_data: Mapping[str, Any] = None):
        """
        Store new item information in database
        :param item_type: One of the types from ItemType
        :param tenant_id: item tenant
        :param item_id: item id
        :param item_data: data to store with item
        """
        logger.info(f"Putting item from DB for item [{item_id}] for tenant [{tenant_id}]")
        keys: ItemKeys = ItemKeys.get_keys(item_type, tenant_id, item_id)
        item = {PK_KEY: keys.primary, ITEM_ID_ATTRIBUTE: item_id}
        if item_data:
            item[DATA_ATTRIBUTE] = item_data
        kwargs = {"Item": item, "ConditionExpression": Attr(PK_KEY).not_exists()}
        try:
            restricted_table(TABLE_NAME, tenant_id).put_item(**kwargs)
        except ClientError as client_error:
            error = client_error.response.get("Error", {})
            error_code = error.get("Code", "")
            logger.error(f"Error Code: [{error_code}]")

            if error_code == "ConditionalCheckFailedException":
                raise ItemConflict(item_type.value, tenant_id, item_id) from client_error
            raise

    @staticmethod
    @start_span("database_get_item")
    def get_item(item_type: ItemType, tenant_id: str, item_id: str, fields=None) -> dict[str, Any]:
        """
        Read item of the given type from database
        :param item_type: One of the types from ItemType
        :param tenant_id: item tenant
        :param item_id: item id
        :param fields: optional parameter to specify fields that should be returned for item
        :return: item's data
        """
        logger.info(f"Fetching {item_type.value} [{item_id}] from DB for tenant: [{tenant_id}]")

        keys: ItemKeys = ItemKeys.get_keys(item_type, tenant_id, item_id)
        kwargs: dict[str, Any] = {"Key": {PK_KEY: keys.primary}}

        if fields:
            kwargs.update(projection_expression(fields, path_prefix=DATA_ATTRIBUTE))

        response = restricted_table(TABLE_NAME, tenant_id).get_item(**kwargs)

        if response.get("Item") is None:
            raise ItemNotFound(item_type.value, tenant_id, item_id)

        return response.get("Item").get("data")

    @staticmethod
    @start_span("database_update_item")
    def update_item(item_type: ItemType, tenant_id: str, item_id: str, item_data: Mapping[str, Any] = None):
        """
        Store updated item information in database
        :param item_type: One of the types from ItemType
        :param tenant_id: item tenant
        :param item_id: item id
        :param item_data: data to store with item
        """
        logger.info(f"Updating item [{item_id}] for tenant [{tenant_id}]")
        keys: ItemKeys = ItemKeys.get_keys(item_type, tenant_id, item_id)
        item = {DATA_ATTRIBUTE: item_data}
        logger.info(f"Value of {item_data=}")
        logger.info(f"Value of {item[DATA_ATTRIBUTE]=}")
        updates = update_expression(update=item, partial_update=True)
        kwargs = {
            "ConditionExpression": Attr(PK_KEY).exists(),
            "Key": {PK_KEY: keys.primary},
        }
        kwargs.update(updates)

        try:
            restricted_table(TABLE_NAME, tenant_id).update_item(**kwargs)
        except ClientError as client_error:
            error = client_error.response.get("Error", {})
            error_code = error.get("Code", "")
            logger.error(f"Error Code: [{error_code}]")

            if error_code == "ConditionalCheckFailedException":
                raise ItemConflict(item_type.value, tenant_id, item_id) from client_error
            raise
