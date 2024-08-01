from .._models import BaseModel

__all__ = ["ArtifactVersion", "ArtifactVersionDeleted"]


class ArtifactVersion(BaseModel):
    id: str
    created_at: str
    name: str
    description: bool


class ArtifactVersionDeleted(BaseModel):
    id: str
    created_at: str
    name: str
    description: bool
