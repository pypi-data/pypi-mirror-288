# pylint: disable=too-few-public-methods

"""Base model definitions for SDK and service."""

from pydantic import BaseModel, Extra


class SDKResponseBaseModel(BaseModel):
    """Base model for SDK response objects. Ignores extra fields."""

    class Config:
        extra = Extra.ignore
        validate_assignment = True
        frozen = True
        validate_all = True


class SDKRequestBaseModel(BaseModel):
    """Base model for SDK request objects. Forbids extra fields."""

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        frozen = True
        validate_all = True
