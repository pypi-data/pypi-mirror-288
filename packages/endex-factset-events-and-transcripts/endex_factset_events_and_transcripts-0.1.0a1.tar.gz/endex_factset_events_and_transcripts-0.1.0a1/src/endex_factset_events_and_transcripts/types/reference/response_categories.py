# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ResponseCategories", "Data"]


class Data(BaseModel):
    category: Optional[str] = None
    """category"""

    description: Optional[str] = None
    """description"""

    subject: Optional[str] = None
    """subject code"""


class ResponseCategories(BaseModel):
    data: Optional[List[Data]] = None
    """Collection of data elements."""
