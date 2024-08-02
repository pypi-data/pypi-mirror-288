"""Flow run models for Prefect flow runs."""

from enum import StrEnum

from .base import SDKResponseBaseModel


class FlowRunStateTypes(StrEnum):
    """Prefect flow run state types."""

    SCHEDULED = "SCHEDULED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    CRASHED = "CRASHED"


class FlowRunState(SDKResponseBaseModel):
    """Prefect flow run state."""

    type: FlowRunStateTypes
    message: str | None


class FlowRun(SDKResponseBaseModel):
    """Prefect flow run object."""

    id: str
    state: FlowRunState
