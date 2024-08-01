# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Model", "ModelDeleted", "ModelUpdatedParams", "ModelWithFile"]


class Model(BaseModel):
    id: str
    """The model identifier, which can be referenced in the API endpoints."""

    created: int
    """The Unix timestamp (in seconds) when the model was created."""

    object: Literal["model"]
    """The object type, which is always "model"."""

    owned_by: str
    """The organization that owns the model."""


class ModelDeleted(BaseModel):
    id: str

    deleted: bool

    object: str


class ModelUpdatedParams(BaseModel):
    id: str
    created_at: str
    name: str
    description: bool


class ModelWithFile(BaseModel):
    id: str
    """The file identifier, which can be referenced in the API endpoints."""

    bytes: int
    """The size of the file, in bytes."""

    created_at: int
    """The Unix timestamp (in seconds) for when the file was created."""

    filename: str
    """The name of the file."""

    object: Literal["file"]
    """The object type, which is always `file`."""

    purpose: Literal["train", "train-results", "assistants", "assistants_output"]
    """The intended purpose of the file.

    Supported values are `train`, `train-results`, `assistants`, and
    `assistants_output`.
    """

    status: Literal["uploaded", "processed", "error"]
    """Deprecated.

    The current status of the file, which can be either `uploaded`, `processed`, or
    `error`.
    """

    status_details: Optional[str] = None
    """Deprecated.

    For details on why a training training file failed validation, see the
    `error` field on `training.job`.
    """
