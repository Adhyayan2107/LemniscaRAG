def evaluate_answer(answer, chunks_retrieved):
    flags = []

    refusal_phrases = [
        "i don't have",
        "cannot find",
        "not mentioned",
        "no information"
    ]

    if chunks_retrieved == 0 and answer:
        flags.append("no_context")

    if any(p in answer.lower() for p in refusal_phrases):
        flags.append("refusal")

    if any(w in answer.lower() for w in ["conflicting", "inconsistent", "varies"]):
        flags.append("pricing_uncertainty")

    return flags