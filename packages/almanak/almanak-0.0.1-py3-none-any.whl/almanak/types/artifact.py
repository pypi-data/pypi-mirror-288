from typing import Optional, List

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Artifact", "ArtifactDeleted", "ArtifactWithFile", "ArtifactUpdatedParams"]


class ArtifactType(BaseModel):
    value: str

class Metadata(BaseModel):
    tags: List[str]
    input_features: str
    output_structure: str

class VersionArtifact(BaseModel):
    author: str
    date_created: str
    description: Optional[str]
    name: str
    id: str
    uri: Optional[str]
    metadata: Metadata

class Artifact(BaseModel):
    id: str
    name: str
    author: str
    date_created: str
    description: str
    is_public: bool
    pending_public_approval: bool
    metadata: Metadata
    artifact_type: ArtifactType
    latest_public_version_artifact: Optional[VersionArtifact]
    latest_registered_production_version_artifact: Optional[VersionArtifact]
    latest_registered_staging_version_artifact: Optional[VersionArtifact]
    latest_version_artifact: Optional[VersionArtifact]


class ArtifactDeleted(BaseModel):
    id: str

    deleted: bool

    object: str


class ArtifactUpdatedParams(BaseModel):
    id: str
    created_at: str
    name: str
    description: bool


class ArtifactWithFile(BaseModel):
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
