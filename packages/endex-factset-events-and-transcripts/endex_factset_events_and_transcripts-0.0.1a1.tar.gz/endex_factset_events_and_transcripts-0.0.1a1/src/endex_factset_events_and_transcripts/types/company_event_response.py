# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CompanyEventResponse", "Data"]


class Data(BaseModel):
    company_name: Optional[str] = FieldInfo(alias="companyName", default=None)
    """The official name of the company."""

    contact_email: Optional[str] = FieldInfo(alias="contactEmail", default=None)
    """Contact email for inquiries related to the event."""

    contact_name: Optional[str] = FieldInfo(alias="contactName", default=None)
    """Name of the contact person for queries related to the event."""

    contact_phone: Optional[str] = FieldInfo(alias="contactPhone", default=None)
    """Contact phone number for inquiries related to the event."""

    description: Optional[str] = None
    """Brief description of the event."""

    event_date_time: Optional[datetime] = FieldInfo(alias="eventDateTime", default=None)
    """Event start time as date/time string according to ISO 8601."""

    event_id: Optional[str] = FieldInfo(alias="eventId", default=None)
    """Unique identifier for the event."""

    event_type: Optional[
        Literal[
            "Earnings",
            "SalesRevenueCall",
            "GuidanceCall",
            "AnalystsInvestorsMeeting",
            "ShareholdersMeeting",
            "SpecialSituation",
            "ConferencePresentation",
            "ConfirmedEarningsRelease",
            "SalesRevenueRelease",
            "ProjectedEarningsRelease",
            "Split",
            "Dividend",
        ]
    ] = FieldInfo(alias="eventType", default=None)
    """Type/Category of the event based on a predefined list."""

    fiscal_period: Optional[str] = FieldInfo(alias="fiscalPeriod", default=None)
    """The fiscal period of the company to which the event pertains."""

    fiscal_year: Optional[str] = FieldInfo(alias="fiscalYear", default=None)
    """The fiscal year of the company to which the event pertains."""

    ir_link: Optional[str] = FieldInfo(alias="irLink", default=None)
    """Link to the ir page of the company."""

    market_time_code: Optional[str] = FieldInfo(alias="marketTimeCode", default=None)
    """Timing code related to opening or closing of market."""

    ticker: Optional[str] = None
    """Ticker-region identifier for the company hosting the event."""

    webcast_link: Optional[str] = FieldInfo(alias="webcastLink", default=None)
    """Link to the webcast of the event."""


class CompanyEventResponse(BaseModel):
    data: Optional[List[Data]] = None
