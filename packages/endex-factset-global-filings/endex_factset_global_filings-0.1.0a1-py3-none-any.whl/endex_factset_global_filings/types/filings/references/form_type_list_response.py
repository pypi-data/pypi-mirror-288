# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["FormTypeListResponse", "Data"]


class Data(BaseModel):
    description: Optional[str] = None
    """source description"""

    form_type: Optional[str] = FieldInfo(alias="formType", default=None)
    """formType"""

    source: Optional[str] = None
    """source"""


class FormTypeListResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Data Array Object"""
