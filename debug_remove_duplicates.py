"""Debug remove_duplicates action in environment"""
from env.environment import DataCleaningEnv
from env.models import Action
from env.tasks import get_tasks
import pandas as pd

# Get the medium_duplicates task
tasks = get_tasks()
dup_task = [t for t in tasks if t['name'] == 'medium_duplicates'][0]

print("=" * 60)
print("DEBUGGING: remove_duplicates ACTION")
print("=" * 60)

print("\n[ORIGINAL TASK DATA]")
print(dup_task['data'])
print(f"DataFrame shape: {dup_task['data'].shape}")
print(f"Data types: {dup_task['data'].dtypes}")

# Create environment and load data
env = DataCleaningEnv()
env.load_dataframe(dup_task['data'].copy())

print("\n[ENVIRONMENT STATE BEFORE ACTION]")
print(f"Data shape: {env.data.shape}")
print(f"Data types: {env.data.dtypes}")
print("Data:")
print(env.data)

print("\n[CHECKING FOR DUPLICATES]")
print(f"Names column exists: {'name' in env.data.columns}")
if 'name' in env.data.columns:
    names = env.data['name'].tolist()
    print(f"Names: {names}")
    print(f"Unique names: {set(names)}")
    print(f"Has duplicates: {len(names) != len(set(names))}")
    print(f"Value counts:\n{env.data['name'].value_counts()}")

print("\n[APPLYING remove_duplicates ACTION]")
before_len = len(env.data)
print(f"Length before: {before_len}")

# Apply the action
obs, reward, done, _ = env.step(Action(action_type="remove_duplicates"))

after_len = len(env.data)
print(f"Length after: {after_len}")
print(f"Reward received: {reward.score}")
print(f"Expected reward: {0.4 if after_len < before_len else 0.0}")

print("\n[DATA AFTER ACTION]")
print(env.data)

print("\n[FINAL STATE]")
final_state = env.state()
print(f"Final state length: {len(final_state)}")
print("Final state:")
for i, row in enumerate(final_state):
    print(f"  {i}: {row}")