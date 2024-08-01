from __future__ import annotations

from .artifacts import Artifacts
from .models import Models
from ..._compat import cached_property
from ..._resource import SyncAPIResource

__all__ = ["Library"]


class Library(SyncAPIResource):
    @cached_property
    def artifacts(self) -> Artifacts:
        return Artifacts(self._client)

    @cached_property
    def models(self) -> Models:
        return Models(self._client)
