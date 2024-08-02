# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["FilingCountResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None
    """id"""

    count: Optional[str] = None
    """source value"""

    source: Optional[str] = None
    """source"""


class FilingCountResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Data Array Object"""
