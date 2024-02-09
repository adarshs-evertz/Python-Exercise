"""
API Gateway Handlers
--------------------

This module contains functions that handle incoming invocations from API Gateway
"""
from http import HTTPStatus

from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError
from evertz_io_identity_lib.event import get_identity_from_event
from evertz_io_observability.decorators import join_trace
from evertz_io_observability.otel_collector import export_trace
from evertz_io_observability.target_services import ExportService
from lambda_event_sources.event_sources import EventSource

from context import logger
from db import Db
from errors import ItemNotFound
from models import ErrorsBody, Headers, Item, ItemModel
from service import Service


# pylint: disable=no-value-for-parameter
@export_trace(export_service=ExportService.OTEL_COLLECTOR_LAYER)
@join_trace(event_source=EventSource.API_GATEWAY_REQUEST)
@event_parser(model=ItemModel)
def create_item(event: ItemModel, context: LambdaContext) -> dict:
    """
    Create item

    :param event: event with data to process
    :param context: lambda execution context
    """
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")

    identity = get_identity_from_event(event=event.dict(), verify=False)
    tenant_id = identity.tenant
    item_data = event.body

    # Database served as dependency injection here, so it will be easier to test this or mock it base on level 0
    service = Service(Db(), tenant_id, identity.sub)
    logger.info(f"Creating Item {item_data}")
    logger.info(f"With Tenant Context: [{tenant_id}]")
    item = service.create_item(item=item_data)
    return {
        "statusCode": HTTPStatus.OK,
        "headers": Headers(content_type="application/vnd.api+json", location=f"items/{item['id']}").dict(by_alias=True),
        "body": Item(**item).json(),
    }


# pylint: disable=no-value-for-parameter
@export_trace(export_service=ExportService.OTEL_COLLECTOR_LAYER)
@join_trace(event_source=EventSource.API_GATEWAY_REQUEST)
@event_parser(model=ItemModel)
def get_item(event: ItemModel, context: LambdaContext) -> dict:
    """
    Retrieve an item

    :param event: event with data to process
    :param context: lambda execution context
    """
    logger.info(f"Event: {event}")
    logger.info(f"Context: {context}")
    identity = get_identity_from_event(event=event.dict(), verify=False)
    path_parameters = event.path_parameters
    item_id = path_parameters.item_id
    tenant_id = identity.tenant
    request_id = event.requestContext.requestId

    logger.info(f"Getting Item: [{item_id}]")
    logger.info(f"With Tenant Context: [{tenant_id}]")

    # Database served as dependency injection here, so it will be easier to test this or mock it base on level 0
    service = Service(Db(), tenant_id, identity.sub)
    try:
        existing_item = service.get_item(item_id=item_id)
        response = {
            "statusCode": HTTPStatus.OK,
            "headers": Headers(content_type="application/vnd.api+json").dict(by_alias=True),
            "body": Item(**existing_item).json(),
        }
    except ItemNotFound as error:
        error_context = {
            "id": request_id,
            "code": error.code,
            "title": error.title,
            "detail": error.msg,
            "status": "404",
        }
        response = {
            "statusCode": HTTPStatus.NOT_FOUND,
            "headers": Headers(content_type="application/vnd.api+json").dict(by_alias=True),
            "body": ErrorsBody(errors=[error_context]).json(),
        }
    except ClientError as error:
        error_context = {
            "id": request_id,
            "code": 400,
            "title": "Unknown error",
            "detail": error.args[0],
            "status": "400",
        }
        response = {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "headers": Headers(content_type="application/vnd.api+json").dict(by_alias=True),
            "body": ErrorsBody(errors=[error_context]).json(),
        }
    return response
