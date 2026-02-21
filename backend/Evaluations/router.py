def classify_query(question: str) -> str:
    words = question.lower().split()
    word_count = len(words)

    complex_keywords = [
        "how", "why", "compare", "difference",
        "explain", "impact", "analyze"
    ]

    has_complex_keyword = any(k in words for k in complex_keywords)
    multiple_questions = question.count("?") > 1
    multi_clause = " and " in question.lower() and "," in question

    if (
        word_count >= 12
        or has_complex_keyword
        or multiple_questions
        or multi_clause
    ):
        return "complex"

    return "simple"