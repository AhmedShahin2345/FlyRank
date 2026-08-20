from enum import Enum

from pydantic import BaseModel, Field


class BookCategory(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    self_help = "self_help"
    children = "children"
    other = "other"


class QualityFlag(str, Enum):
    no_description = "no_description"
    price_is_zero = "price_is_zero"
    title_looks_like_marketing = "title_looks_like_marketing"
    summary_is_a_guess = "summary_is_a_guess"


class EnrichInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    price_gbp: float = Field(ge=0, le=100000)


class EnrichOutput(BaseModel):
    category: BookCategory
    summary: str = Field(min_length=1, max_length=200)
    confidence: float = Field(ge=0, le=1)
    quality_flags: list[QualityFlag] = Field(max_length=4)