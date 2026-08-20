from pydantic import BaseModel, Field
from typing import List, Optional

class Category(str, Enum):
    FICTION = "fiction"
    NONFICTION = "nonfiction"
    SELF_HELP = "self_help"
    CHILDREN = "children"
    OTHER = "other"

class EnrichInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field("", max_length=2000)
    price_gbp: float = Field(..., ge=0)

class QualityFlag(str, Enum):
    NO_DESCRIPTION = "no_description"
    PRICE_IS_ZERO = "price_is_zero"
    TITLE_LOOKS_LIKE_MARKETING = "title_looks_like_marketing"
    SUMMARY_IS_A_GUESS = "summary_is_a_guess"

class EnrichOutput(BaseModel):
    category: Category
    summary: str = Field(..., min_length=1, max_length=200)
    confidence: float = Field(..., ge=0.0, le=1.0)
    quality_flags: List[QualityFlag] = Field(default_factory=list)
