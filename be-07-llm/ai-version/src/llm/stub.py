from .schema import EnrichOutput, Category, QualityFlag

def stub_answer():
    return EnrichOutput(
        category=Category.OTHER,
        summary="Stubbed response",
        confidence=0.9,
        quality_flags=[QualityFlag.SUMMARY_IS_A_GUESS]
    )

def fallback_answer():
    return EnrichOutput(
        category=Category.OTHER,
        summary="Fallback response",
        confidence=0.1,
        quality_flags=[QualityFlag.SUMMARY_IS_A_GUESS]
    )
