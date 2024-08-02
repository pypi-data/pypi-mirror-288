# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FilingSearchParams"]


class FilingSearchParams(TypedDict, total=False):
    sources: Required[List[str]]
    """Code for document source to include.

    This is a comma-separated list. Use the `/reference/sources` endpoint to get the
    list of available sources.
    """

    _pagination_limit: Annotated[int, PropertyInfo(alias="_paginationLimit")]
    """Number of results to return per page."""

    _pagination_offset: Annotated[int, PropertyInfo(alias="_paginationOffset")]
    """Page number of the results to return."""

    categories: List[str]
    """Code for categories to include.

    This is a comma-separated list. Use the `/reference/categories` endpoint to get
    the list of available categories.

    Default = All categories.
    """

    edgar_accession: Annotated[str, PropertyInfo(alias="edgarAccession")]
    """A unique identifier given to each EDGAR filings document.

    e.g. accession=0001013237-21-000069&sources=EDG.

    **Note: When used in conjunction with the 'source' parameter set to 'EDGAR', the
    API considers this accession for data retrieval. For non-EDGAR sources, this
    parameter is ignored.**
    """

    edgar_form_type: Annotated[str, PropertyInfo(alias="edgarFormType")]
    """Restricts the search to include any form types of EDGAR.

    **Note:This parameter applies exclusively to EDGAR searches; it is ignored when
    used with non-EDGAR sources.**
    """

    end_date: Annotated[str, PropertyInfo(alias="endDate")]
    """End Date. Format is YYYYMMDD or relative +/- days (0,-1,etc)."""

    ids: List[str]
    """Requested symbols or securities.

    This is a comma-separated list with a maximum limit of 1000. Each symbol can be
    a FactSet exchange symbol, CUSIP, or SEDOL.
    """

    primary_id: Annotated[Literal[True, False], PropertyInfo(alias="primaryId")]
    """Type of identifier search

    - true - Returns headlines of stories that have the searched identifier(s) as
      the primary identifier.
    - false - Returns headlines of stories that mentioned or referred to the
      identifier.
    """

    search_text: Annotated[str, PropertyInfo(alias="searchText")]
    """
    Restricts the search to include only document stories which include the text
    searched.
    """

    sort: Literal["asc", "desc"]
    """
    Sorting the results in chronological (oldest to newest) or reverse chronological
    (newest to oldest) order.

    - desc - sorting results in reverse chronological (descending) order. This is
      the default value if the sort parameter isn't used in the query.
    - asc - sorting results in chronological (ascending) order. If a start date is
      not specified, the API has a 10-year searching limitation.
    """

    start_date: Annotated[str, PropertyInfo(alias="startDate")]
    """Start Date. Format is YYYYMMDD or relative +/- days (0,-1,etc).

    **Note:** **The API supports data from 1995 onwards. Ensure that the provided
    Date falls within this range for accurate results.**
    """

    time_zone: Annotated[str, PropertyInfo(alias="timeZone")]
    """
    timeZone to return story dates and times.Time zones, represented in POSIX
    format, are automatically adjusted for daylight savings. timeZone names are
    sourced from the IANA timezone registry.
    """
