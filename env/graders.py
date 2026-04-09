from typing import List, Dict, Any


def safe_score(score: float) -> float:
    """Ensure score is strictly between 0 and 1, never 0.0 or 1.0"""
    return max(0.1, min(0.9, score))


def normalize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float) and value != value:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.isdigit():
            return int(value)
        lower = value.lower()
        if lower == "nan":
            return None
        return lower
    return value


def compare_records(actual: List[Dict[str, Any]], expected: List[Dict[str, Any]]) -> float:
    if not actual or not expected:
        return 0.0

    matches = 0
    total = 0

    for act_row, exp_row in zip(actual, expected):
        if not isinstance(act_row, dict) or not isinstance(exp_row, dict):
            continue
        for key in exp_row.keys():
            total += 1
            act_value = normalize_value(act_row.get(key))
            exp_value = normalize_value(exp_row.get(key))
            if act_value == exp_value:
                matches += 1

    if total == 0:
        return 0.0
    return round(matches / total, 2)


def grade_task(actual: List[Dict[str, Any]], expected: List[Dict[str, Any]]) -> float:
    score = compare_records(actual, expected)
    return min(max(score, 0.0), 1.0)


def grade_hard(data):
    score = 0.0

    # Check missing values
    no_nulls = all(
        all(v is not None for v in row.values())
        for row in data
    )
    if no_nulls:
        score += 0.3

    # Check normalization (names lowercase + no spaces)
    normalized = all(
        row.get("name", "").strip() == row.get("name", "").lower()
        for row in data if "name" in row
    )
    if normalized:
        score += 0.3

    # Check duplicates (no duplicate names)
    names = [row.get("name") for row in data if "name" in row]
    if len(set(names)) == len(names):
        score += 0.4

    return safe_score(score)


def grade_easy(data):
    score = 0.0
    # Check if age has no None
    ages = [row.get("age") for row in data]
    if all(age is not None for age in ages):
        score = 0.7
    else:
        score = 0.3
    return safe_score(score)


def grade_medium_normalize(data):
    score = 0.0
    names = [row.get("name", "") for row in data]
    normalized = all(name.strip().lower() == name for name in names)
    if normalized:
        score = 0.6
    else:
        score = 0.2
    return safe_score(score)


def grade_medium_missing(data):
    score = 0.0
    no_nulls = all(all(v is not None for v in row.values()) for row in data)
    if no_nulls:
        score = 0.8
    else:
        score = 0.4
    return safe_score(score)


def grade_easy_normalize(data):
    score = 0.0
    names = [row.get("name", "") for row in data]
    normalized = all(name.strip().lower() == name for name in names)
    if normalized:
        score = 0.6
    else:
        score = 0.2
    return safe_score(score)


def grade_medium_duplicates(data):
    score = 0.0
    names = [row.get("name") for row in data if "name" in row]
    if len(set(names)) == len(names):
        score = 0.7
    else:
        score = 0.3
    return safe_score(score)


def grade_hard_complex(data):
    # Similar to grade_hard but for more complex data
    score = 0.0

    no_nulls = all(
        all(v is not None for v in row.values())
        for row in data
    )
    if no_nulls:
        score += 0.3

    normalized = all(
        row.get("name", "").strip() == row.get("name", "").lower()
        for row in data if "name" in row
    )
    if normalized:
        score += 0.3

    names = [row.get("name") for row in data if "name" in row]
    if len(set(names)) == len(names):
        score += 0.4

    return safe_score(score)
