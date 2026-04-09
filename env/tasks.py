import pandas as pd
from typing import List, Dict, Any


def get_tasks() -> List[Dict[str, Any]]:
    return [
        {
            "name": "easy",
            "task": "easy_data_cleaning",
            "difficulty": "easy",
            "action_sequence": ["fill_missing"],
            "data": pd.DataFrame([
                {"name": "John", "age": "25", "salary": 50000},
                {"name": "Alice", "age": None, "salary": 60000}
            ]),
        },
        {
            "name": "medium_normalize",
            "task": "medium_data_cleaning",
            "difficulty": "medium",
            "action_sequence": ["normalize"],
            "data": pd.DataFrame([
                {"name": " John ", "age": "25", "salary": 50000},
                {"name": "JOHN", "age": "30", "salary": 70000},
                {"name": "bob", "age": "28", "salary": 55000}
            ]),
        },
        {
            "name": "medium_missing",
            "task": "medium_missing_cleaning",
            "difficulty": "medium",
            "action_sequence": ["fill_missing"],
            "data": pd.DataFrame([
                {"name": "John", "age": None, "salary": 50000},
                {"name": "Alice", "age": "28", "salary": None},
                {"name": "Bob", "age": None, "salary": 55000}
            ]),
        },
        {
            "name": "hard",
            "task": "hard_data_cleaning",
            "difficulty": "hard",
            "action_sequence": ["fill_missing", "normalize", "remove_duplicates"],
            "data": pd.DataFrame([
                {"name": "John ", "age": "25", "salary": None},
                {"name": "john", "age": "twenty five", "salary": 50000},
                {"name": "Alice", "age": None, "salary": 60000},
                {"name": "John ", "age": "25", "salary": None},
                {"name": "BOB", "age": "30", "salary": None}
            ]),
        },
        {
            "name": "hard_complex",
            "task": "hard_complex_cleaning",
            "difficulty": "hard",
            "action_sequence": ["fill_missing", "normalize", "remove_duplicates"],
            "data": pd.DataFrame([
                {"name": " Alice ", "age": None, "salary": None},
                {"name": "alice", "age": "28", "salary": 70000},
                {"name": " Alice ", "age": None, "salary": None},
                {"name": "John", "age": None, "salary": 50000},
                {"name": "john", "age": "thirty five", "salary": None},
                {"name": "John", "age": None, "salary": 50000},
                {"name": "Bob", "age": "42", "salary": None},
                {"name": "bob", "age": None, "salary": None}
            ]),
        },
        {
            "name": "easy_normalize",
            "task": "easy_normalize_cleaning",
            "difficulty": "easy",
            "action_sequence": ["normalize"],
            "data": pd.DataFrame([
                {"name": "JOHN", "age": "25", "salary": 50000},
                {"name": "alice", "age": "30", "salary": 60000}
            ]),
        },
        {
            "name": "medium_duplicates",
            "task": "medium_duplicates_cleaning",
            "difficulty": "medium",
            "action_sequence": ["remove_duplicates"],
            "data": pd.DataFrame([
                {"name": "John", "age": "25", "salary": 50000},
                {"name": "Alice", "age": "30", "salary": 60000},
                {"name": "John", "age": "25", "salary": 50000},
                {"name": "Bob", "age": "28", "salary": 55000}
            ]),
        }
    ]
