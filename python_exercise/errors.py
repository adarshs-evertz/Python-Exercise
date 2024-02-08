"""Errors Specific to Items."""
from http import HTTPStatus
from re import findall


class ItemErrorBase(Exception):
    """Base Class For Tenant Errors"""

    code: str
    title: str
    http_code: HTTPStatus

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not getattr(cls, "code", None):
            cls.code: str = cls.__name__

        if not getattr(cls, "title", None):
            cls.title: str = " ".join(findall("[A-Z][^A-Z]*", cls.__name__))


class ItemNotFound(ItemErrorBase):
    """
    Raised when an Item was not found
    """

    http_code = HTTPStatus.NOT_FOUND

    def __init__(self, item_type: str, tenant: str, item_id: str):
        self.msg = f"Item of type {item_type} [{tenant}/{item_id}] not found."
        super().__init__(self.msg)


class ItemConflict(ItemErrorBase):
    """
    Raised when adding or modifying this `Item` would conflict with an already
    existing `Item`
    """

    http_code = HTTPStatus.CONFLICT

    def __init__(self, item_type: str, tenant: str, item_id: str):
        self.msg = f"Item of type {item_type} [{tenant}:{item_id}] already exists."
        super().__init__(self.msg)
