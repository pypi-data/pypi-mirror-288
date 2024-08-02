# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["HistoryRetrieveParams"]


class HistoryRetrieveParams(TypedDict, total=False):
    year: Required[int]
    """
    Specifies the year for which the historical audio recordings and related
    metadata are to be retrieved.
    """

    trimmed: bool
    """Specifies if trimmed/untrimmed historical audio recordings should be returned."""
