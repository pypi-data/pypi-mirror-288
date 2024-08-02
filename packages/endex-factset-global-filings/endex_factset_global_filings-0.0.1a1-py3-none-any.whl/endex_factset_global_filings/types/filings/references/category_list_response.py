# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...._models import BaseModel

__all__ = ["CategoryListResponse", "Data"]


class Data(BaseModel):
    category: Optional[str] = None
    """category"""

    description: Optional[str] = None
    """description"""

    subject: Optional[str] = None
    """subject code"""


class CategoryListResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Data Array Object"""
