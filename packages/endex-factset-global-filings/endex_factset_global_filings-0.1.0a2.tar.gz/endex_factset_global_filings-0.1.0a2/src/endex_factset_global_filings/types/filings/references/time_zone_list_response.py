# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["TimeZoneListResponse", "Data"]


class Data(BaseModel):
    time_zone: Optional[str] = FieldInfo(alias="timeZone", default=None)
    """timeZone"""


class TimeZoneListResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Data Array Object"""
