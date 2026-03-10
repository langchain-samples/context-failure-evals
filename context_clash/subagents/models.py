from typing import Literal

from pydantic import BaseModel, Field


class CompanyInfo(BaseModel):
    """Extracted company information."""

    ceo_name: str | None = Field(default=None, description="Name of the CEO")
    cto_name: str | None = Field(
        default=None, description="Name of the CTO (if available)"
    )
    employee_headcount: str | None = Field(
        default=None,
        description="Employee count as string, possibly a range (e.g., '150', '100-200', '500+')",
    )
    funding_status: (
        Literal[
            "bootstrapped",
            "pre-seed",
            "seed",
            "series_a",
            "series_b",
            "series_c",
            "series_d",
            "series_e_plus",
            "public",
            "acquired",
            "private",
        ]
        | None
    ) = Field(
        default=None,
        description="Funding stage of the company. If the company was acquired, just return 'acquired'.",
    )
    total_funding_raised: float | None = Field(
        default=None,
        description="Total funding raised in millions USD",
    )
    year_founded: int | None = Field(
        default=None, description="Year the company was founded"
    )
    office_locations: list[str] = Field(
        default_factory=list,
        description="List of office location cities in alphabetical order. Use full city names, e.g. New York City, not just New York. Do not add country or state.",
    )
    confidence_notes: str | None = Field(
        default=None,
        description="Notes about confidence level or data sources for the extracted information",
    )
    source: (
        Literal[
            "company_homepage",
            "crunchbase",
            "glassdoor",
            "linkedin",
            "news",
            "pitchbook",
            "twitter",
            "wikipedia",
            "aggregated",
        ]
        | None
    ) = Field(
        default=None,
        description="Source of the information",
    )
    confirm_read_files: str = Field(
        description="Confirm that you have read all relevant files for your source. If no files were read with the read_file tool call, explain why.",
    )
