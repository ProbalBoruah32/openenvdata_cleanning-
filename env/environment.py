import pandas as pd
from env.models import Observation, Action, Reward


class DataCleaningEnv:
    def __init__(self):
        self.max_steps = 5
        self.step_count = 0
        self.data = pd.DataFrame([])
        self.reset()

    def reset(self):
        self.step_count = 0

        self.data = pd.DataFrame([
            {"name": "John ", "age": "25", "salary": None},
            {"name": "john", "age": "twenty five", "salary": 50000},
            {"name": "Alice", "age": None, "salary": 60000}
        ])

        return self._get_observation()

    def load_dataframe(self, df: pd.DataFrame):
        self.step_count = 0
        self.data = df.copy()
        return self._get_observation()

    def step(self, action: Action):
        self.step_count += 1
        reward = 0.0

        if action.action_type == "fill_missing":
            filled = self._fill_missing()
            if filled > 0:
                reward += min(0.4, 0.15 + filled * 0.05)

        elif action.action_type == "normalize":
            normalized = self._normalize_columns()
            if normalized > 0:
                reward += min(0.4, 0.15 + normalized * 0.02)

        elif action.action_type == "remove_duplicates":
            removed = self._remove_duplicates()
            if removed > 0:
                reward += min(0.4, 0.15 + removed * 0.05)

        done = self.step_count >= self.max_steps
        return self._get_observation(), Reward(score=reward), done, {}

    def _fill_missing(self) -> int:
        changes = 0
        for col in self.data.columns:
            if pd.api.types.is_numeric_dtype(self.data[col]):
                before_missing = self.data[col].isna().sum()
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                if self.data[col].isna().sum() > 0:
                    mean_value = self.data[col].mean()
                    if pd.notna(mean_value):
                        self.data[col] = self.data[col].fillna(mean_value)
                        changes += before_missing - self.data[col].isna().sum()
            else:
                self.data[col] = self.data[col].astype(str).replace({'nan': pd.NA})
                before_missing = self.data[col].isna().sum()
                mode_values = self.data[col].dropna()
                if not mode_values.empty:
                    fill_value = mode_values.mode().iloc[0]
                else:
                    fill_value = "unknown"
                self.data[col] = self.data[col].fillna(fill_value).replace("<NA>", fill_value)
                changes += before_missing - self.data[col].isna().sum()
        return int(changes)

    def _normalize_columns(self) -> int:
        changes = 0
        for col in self.data.columns:
            if self.data[col].dtype == object or pd.api.types.is_string_dtype(self.data[col]):
                original = self.data[col].astype(str)
                normalized = (original
                              .str.strip()
                              .str.replace(r"\s+", " ", regex=True)
                              .str.lower())
                self.data[col] = normalized
                changes += (original != normalized).sum()
            else:
                coerced = pd.to_numeric(self.data[col], errors='coerce')
                if coerced.notna().any():
                    self.data[col] = coerced
        return int(changes)

    def _remove_duplicates(self) -> int:
        before = len(self.data)
        self.data = self.data.drop_duplicates(keep='first')
        after = len(self.data)
        return before - after

    def state(self):
        return self._clean_records(self.data.to_dict(orient="records"))

    def _get_observation(self):
        return Observation(
            data=self._clean_records(self.data.to_dict(orient="records")),
            step_count=self.step_count
        )

    @staticmethod
    def _clean_records(records):
        cleaned = []
        for record in records:
            cleaned.append({
                key: None if pd.isna(value) else value
                for key, value in record.items()
            })
        return cleaned
