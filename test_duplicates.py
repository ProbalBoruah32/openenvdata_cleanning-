"""Test script to debug remove_duplicates grading issue"""
from env.environment import DataCleaningEnv
from env.models import Action
from env.tasks import get_tasks
from env.graders import grade_medium_duplicates, safe_score

# Get the medium_duplicates task
tasks = get_tasks()
dup_task = [t for t in tasks if t['name'] == 'medium_duplicates'][0]

print("=" * 60)
print("Testing: medium_duplicates_cleaning")
print("=" * 60)

print("\n[INITIAL DATA]")
print(dup_task['data'])
print(f"Initial rows: {len(dup_task['data'])}")

# Run the environment
env = DataCleaningEnv()
env.load_dataframe(dup_task['data'].copy())

print("\n[BEFORE CLEANING]")
state_before = env.state()
print(f"State before: {state_before}")
print(f"Names: {[r.get('name') for r in state_before]}")

# Apply action
print("\n[APPLYING ACTION: remove_duplicates]")
obs, reward, done, _ = env.step(Action(action_type="remove_duplicates"))
print(f"Reward from action: {reward.score}")

# Get final state
print("\n[AFTER CLEANING]")
final_state = env.state()
print(f"State after: {final_state}")
print(f"Rows after: {len(final_state)}")
print(f"Names: {[r.get('name') for r in final_state]}")

# Grade it
print("\n[GRADING]")
raw_score = grade_medium_duplicates(final_state)
print(f"Raw score from grader: {raw_score}")
final_score = safe_score(float(raw_score))
print(f"After safe_score: {final_score}")

print("\n[DUPLICATE CHECK]")
names = [r.get('name') for r in final_state if 'name' in r]
print(f"Names in final state: {names}")
print(f"Unique names: {set(names)}")
print(f"Has duplicates: {len(set(names)) != len(names)}")
print(f"Score should be: 0.7 if no duplicates, 0.3 if duplicates")
print(f"Actual score: {final_score}")
