from __future__ import annotations

import httpx
from typing_extensions import Literal

from ...._base_client import (
    make_request_options,
)
from ...._resource import SyncAPIResource
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from ...._utils import (
    maybe_transform,
)
from ....pagination import SyncCursorPage
from ....types.artifact_version import ArtifactVersion, ArtifactVersionDeleted
from ....types.file_create_params import FileCreateParams
from ....types.file_list_params import FileListParams

__all__ = [
    "Versions",
]


class Versions(SyncAPIResource):
    def create(
        self,
        artifact_name: str,
        *,
        version_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactVersion:
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        return self._post(
            f"/library/artifacts/{artifact_name}/versions",
            body=maybe_transform({"version_name": version_name}, FileCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ArtifactVersion,
        )

    def retrieve(
        self,
        version_name: str,
        *,
        artifact_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactVersion:
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        if not version_name:
            raise ValueError(
                f"Expected a non-empty value for `version_name` but received {version_name!r}"
            )
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version_name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ArtifactVersion,
        )

    def list(
        self,
        artifact_name: str,
        *,
        after: str | NotGiven = NOT_GIVEN,
        before: str | NotGiven = NOT_GIVEN,
        filter: Literal["in_progress", "completed", "failed", "cancelled"]
        | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[ArtifactVersion]:
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        return self._get_api_list(
            f"/library/artifacts/{artifact_name}/versions",
            page=SyncCursorPage[ArtifactVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after": after,
                        "before": before,
                        "filter": filter,
                        "limit": limit,
                        "order": order,
                    },
                    FileListParams,
                ),
            ),
            model=ArtifactVersion,
        )

    def delete(
        self,
        version_name: str,
        *,
        artifact_name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactVersionDeleted:
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        if not version_name:
            raise ValueError(
                f"Expected a non-empty value for `version_name` but received {version_name!r}"
            )
        return self._delete(
            f"/library/artifacts/{artifact_name}/versions/{version_name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ArtifactVersionDeleted,
        )

    def upload(
        self,
        *,
        artifact_name: str,
        file: FileTypes,
    ) -> ArtifactVersion:
        """Upload a file to the `files` API and then attach it to the given artifact version

        Note the file will be asynchronously processed (you can use the alternative
        polling helper method to wait for processing to complete).
        """
        file_obj = self._client.files.create(file=file, purpose="assistants")
        return self.create(artifact_name=artifact_name, version_name=file_obj.id)

    def list_files(
        self,
        version_name: str,
        *,
        artifact_name: str,
        after: str | NotGiven = NOT_GIVEN,
        before: str | NotGiven = NOT_GIVEN,
        filter: Literal["in_progress", "completed", "failed", "cancelled"]
        | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[ArtifactVersion]:
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        if not version_name:
            raise ValueError(
                f"Expected a non-empty value for `version_name` but received {version_name!r}"
            )
        return self._get_api_list(
            f"/library/artifacts/{artifact_name}/versions/{version_name}/files",
            page=SyncCursorPage[ArtifactVersion],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after": after,
                        "before": before,
                        "filter": filter,
                        "limit": limit,
                        "order": order,
                    },
                    FileListParams,
                ),
            ),
            model=ArtifactVersion,
        )
