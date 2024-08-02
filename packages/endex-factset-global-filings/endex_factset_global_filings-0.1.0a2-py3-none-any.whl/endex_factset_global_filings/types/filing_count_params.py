# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FilingCountParams"]


class FilingCountParams(TypedDict, total=False):
    sources: Required[List[str]]
    """Code for document source to include.This is a comma-separated list.

    Use the `/reference/sources` endpoint to get the list of available sources.
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """End Date. Format is YYYYMMDD or relative +/- days (0,-1,etc)."""

    ids: List[str]
    """Requested symbols or securities.

    This is a comma-separated list with a maximum limit of 1000. Each symbol can be
    a FactSet exchange symbol, CUSIP, or SEDOL.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Start Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

    **Note:** **The API supports data from 1995 onwards. Ensure that the provided
    Date falls within this range for accurate results.**
    """
