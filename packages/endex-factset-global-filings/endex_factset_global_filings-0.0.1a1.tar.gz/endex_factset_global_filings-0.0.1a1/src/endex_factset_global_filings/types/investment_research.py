# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["InvestmentResearch", "Data", "Meta", "MetaPagination"]


class Data(BaseModel):
    accession: Optional[str] = None
    """A unique identifier given to each EDGAR filings document."""

    all_ids: Optional[List[str]] = FieldInfo(alias="allIds", default=None)
    """Refers to all companies mentioned in the document.

    This could also include the primary company id as well.

    **Note:** For the "allIds" and "primaryIds" fields:

    - These identifiers can be either SEDOLs or CUSIPs, depending on the search
      criteria and the type of identifiers specified in your request.
    - The API will return the corresponding identifiers based on the search
      parameters provided.
    """

    categories: Optional[List[str]] = None
    """
    - Comma-separated list of country, industry, and subject codes.
    - Sourced from "/reference/categories" with two-letter codes (SB for subjects,
      IN for industries, LN for languages, CN for countries, RN for regions, DT for
      document types).
    """

    document_id: Optional[str] = FieldInfo(alias="documentId", default=None)
    """Unique identifier for a document."""

    filings_date_time: Optional[str] = FieldInfo(alias="filingsDateTime", default=None)
    """Publish date and time of the latest version (in ISO 8601 format, UTC)."""

    filing_size: Optional[str] = FieldInfo(alias="filingSize", default=None)
    """Filings specific metadata providing info around the size of the document."""

    filings_link: Optional[str] = FieldInfo(alias="filingsLink", default=None)
    """A secure HTTPS link for downloading the associated document."""

    form_type: Optional[str] = FieldInfo(alias="formType", default=None)
    """Filings specific metadata providing info around the form type (e.g.

    8K, 10K, etc.)
    """

    headline: Optional[str] = None
    """Headline of the story, actual time and date of the event."""

    primary_ids: Optional[List[str]] = FieldInfo(alias="primaryIds", default=None)
    """Refers to the main company a particular document refers to."""

    search_ids: Optional[str] = FieldInfo(alias="searchIds", default=None)
    """Returns IDs used in the id's parameter.

    The identifier type is based on what was used in the parameter.
    """

    source: Optional[str] = None
    """
    Provides the source of the document, and the source value is one among those
    provided by the "/reference/sources" endpoint.
    """


class MetaPagination(BaseModel):
    is_estimated_total: Optional[bool] = FieldInfo(alias="isEstimatedTotal", default=None)
    """
    This field acts as a flag for the exact count of results and is defaulted to
    false as the API should always return the exact count of results.
    """

    total: Optional[int] = None
    """Total number of files the API returns for a particular query."""


class Meta(BaseModel):
    pagination: Optional[MetaPagination] = None
    """Pagination Object"""


class InvestmentResearch(BaseModel):
    data: Optional[List[Data]] = None
    """Data Array Object"""

    meta: Optional[Meta] = None
    """Meta Object"""
