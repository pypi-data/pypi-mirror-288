from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["FileCreateParams"]


class FileCreateParams(TypedDict, total=False):
    file: Required[FileTypes]
    """The File object (not file name) to be uploaded."""

    description: str
