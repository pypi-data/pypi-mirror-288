# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CalendarEventCreateParams", "Data", "DataDateTime", "DataUniverse"]


class CalendarEventCreateParams(TypedDict, total=False):
    data: Data


class DataDateTime(TypedDict, total=False):
    end: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """End time of the event in ISO 8601 format.

    The maximum dateTime limit between start and end is upto 90 days.
    """

    start: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """Start time of the event in ISO 8601 format.

    The maximum dateTime limit between start and end is upto 90 days.
    """


class DataUniverse(TypedDict, total=False):
    symbols: Required[List[str]]
    """Companies to return in the response.

    - Only Tickers type can support multiple entries.
    """

    type: Required[Literal["Tickers", "Index", "Etf", "AllCompanies"]]
    """NOTE:

    - Etf: Requires additionl access to get the data.
    - AllCompanies: While using this, we should not pass any symbols in the symbols
      field.
    """


class Data(TypedDict, total=False):
    date_time: Required[Annotated[DataDateTime, PropertyInfo(alias="dateTime")]]
    """
    - Data is available from 2002.
    - If users provide future dates in requests, the API will not return any data.
    """

    universe: Required[DataUniverse]

    event_types: Annotated[
        List[
            Literal[
                "Earnings",
                "SalesRevenueCall",
                "GuidanceCall",
                "AnalystsInvestorsMeeting",
                "ShareholdersMeeting",
                "SpecialSituation",
                "Conference",
                "ConfirmedEarningsRelease",
                "ProjectedEarningsRelease",
                "SalesRevenueRelease",
                "Split",
                "Dividend",
            ]
        ],
        PropertyInfo(alias="eventTypes"),
    ]
    """The type of events returned in the response"""
