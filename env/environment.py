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
            for col in self.data.columns:
                if pd.api.types.is_numeric_dtype(self.data[col]):
                    self.data[col] = self.data[col].fillna(self.data[col].mean())
                else:
                    self.data[col] = self.data[col].ffill().bfill()
            reward += 0.3

        elif action.action_type == "normalize":
            for col in self.data.select_dtypes(include=["object"]).columns:
                self.data[col] = self.data[col].astype(str).str.strip().str.lower()
            reward += 0.3

        elif action.action_type == "remove_duplicates":
            before = len(self.data)
            # Remove duplicates based on 'name' column if it exists, otherwise all columns
            if 'name' in self.data.columns:
                self.data = self.data.drop_duplicates(subset=['name'], keep='first')
            else:
                self.data = self.data.drop_duplicates()
            after = len(self.data)
            if after < before:
                reward += 0.4

        done = self.step_count >= self.max_steps

        return self._get_observation(), Reward(score=reward), done, {}

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
