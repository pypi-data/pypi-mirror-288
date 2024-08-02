# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SourceListResponse", "Data", "DataSourcesObject"]


class DataSourcesObject(BaseModel):
    description: Optional[str] = None
    """source description"""

    source: Optional[str] = None
    """source value"""


class Data(BaseModel):
    sources_object: Optional[DataSourcesObject] = FieldInfo(alias="sourcesObject", default=None)


class SourceListResponse(BaseModel):
    data: Optional[List[Data]] = None
    """Data Array Object"""
