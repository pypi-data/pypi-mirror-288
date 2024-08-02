# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["ByFileNameRetrieveParams"]


class ByFileNameRetrieveParams(TypedDict, total=False):
    file_name: Annotated[str, PropertyInfo(alias="fileName")]
    """This parameter is used to filter the data on based on the file name."""
