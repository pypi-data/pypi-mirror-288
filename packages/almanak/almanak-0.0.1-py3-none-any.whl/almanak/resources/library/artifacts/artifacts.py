from __future__ import annotations

from typing import Mapping, cast, Optional

import httpx

from .versions import Versions
from ...._base_client import (
    make_request_options,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import extract_files, deepcopy_minimal, maybe_transform
from ....pagination import SyncPage
from ....types.artifact import (
    Artifact,
    ArtifactDeleted,
    ArtifactWithFile,
    ArtifactUpdatedParams,
)
from ....types.file_create_params import FileCreateParams

__all__ = ["Artifacts"]


class Artifacts(SyncAPIResource):
    def create(
        self,
        *,
        file: ArtifactWithFile,
        name: str,
        description: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Artifact:
        body = deepcopy_minimal(
            {
                "file": file,
                "description": description,
                "name": name,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        if files:
            # It should be noted that the actual Content-Type header that will be
            # sent to the server will contain a `boundary` parameter, e.g.
            # multipart/form-data; boundary=---abc--
            extra_headers = {
                "Content-Type": "multipart/form-data",
                **(extra_headers or {}),
            }
        return self._post(
            "library/artifacts",
            body=maybe_transform(body, FileCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ArtifactWithFile,
        )

    def retrieve(
        self,
        artifact_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Artifact:
        """
        Retrieves a artifacts instance, providing basic information about the artifacts such as
        the owner and permissioning.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        return self._get(
            f"/library/artifacts/{artifact_name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Artifact,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPage[Artifact]:
        """
        Lists the currently available artifacts, and provides basic information about each
        one such as the owner and availability.
        """
        return self._get_api_list(
            "/library/artifacts/",
            page=SyncPage[Artifact],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            model=Artifact,
        )

    def delete(
        self,
        artifact_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactDeleted:
        """Delete an artifact.

        You must have the Owner role in your organization to
        delete a model.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        return self._delete(
            f"/library/artifacts/{artifact_name}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ArtifactDeleted,
        )

    def update(
        self,
        artifact_name: str,
        *,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Artifact:
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        return self._post(
            f"/library/artifacts/{artifact_name}",
            body=maybe_transform({"metadata": metadata}, ArtifactUpdatedParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Artifact,
        )

    def retrieve_versions(
        self,
        artifact_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Artifact:
        """
        Retrieves an artifact instance, providing basic information about the artifact such as
        the owner and permissioning.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not artifact_name:
            raise ValueError(
                f"Expected a non-empty value for `artifact_name` but received {artifact_name!r}"
            )
        return self._get(
            f"/library/artifact_name/{artifact_name}/versions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Artifact,
        )

    @cached_property
    def versions(self) -> Versions:
        return Versions(self._client)
