from .schema import BookCategory, EnrichInput, EnrichOutput, QualityFlag


def stub_answer(item: EnrichInput) -> EnrichOutput:
    flags = []
    if not item.description.strip():
        flags.append(QualityFlag.no_description)
    if item.price_gbp == 0:
        flags.append(QualityFlag.price_is_zero)
    return EnrichOutput(
        category=BookCategory.other,
        summary="Stub answer — the model call is disabled (LLM_STUB=1).",
        confidence=0.1,
        quality_flags=flags,
    )


def fallback_answer() -> EnrichOutput:
    return EnrichOutput(
        category=BookCategory.other,
        summary="Enrichment is currently disabled (LLM_ENABLED=false).",
        confidence=0.1,
        quality_flags=[QualityFlag.summary_is_a_guess],
    )