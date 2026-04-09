#!/usr/bin/env python3
"""
Diagnostic script to identify the exact issue preventing submission
"""
import sys
from env.tasks import get_tasks
from env.graders import (
    grade_easy, grade_medium_normalize, grade_medium_missing, grade_hard,
    grade_easy_normalize, grade_medium_duplicates, grade_hard_complex, safe_score
)
from env.environment import DataCleaningEnv
from env.models import Action

print("=" * 70)
print("SUBMISSION DIAGNOSTIC CHECK")
print("=" * 70)
print()

# Step 1: Check tasks count
tasks = get_tasks()
print(f"STEP 1: Task Count")
print(f"  Total tasks: {len(tasks)}")
if len(tasks) < 3:
    print(f"  ❌ ERROR: Need at least 3 tasks, found {len(tasks)}")
    sys.exit(1)
print(f"  ✅ PASS: {len(tasks)} tasks (≥ 3)")
print()

# Step 2: Check each task has proper structure
print(f"STEP 2: Task Structure")
grader_map = {
    'easy': grade_easy,
    'medium_normalize': grade_medium_normalize,
    'medium_missing': grade_medium_missing,
    'hard': grade_hard,
    'easy_normalize': grade_easy_normalize,
    'medium_duplicates': grade_medium_duplicates,
    'hard_complex': grade_hard_complex,
}

all_tasks_valid = True
for i, task_config in enumerate(tasks, 1):
    required_fields = ['name', 'task', 'difficulty', 'action_sequence', 'data']
    missing = [f for f in required_fields if f not in task_config]
    if missing:
        print(f"  ❌ Task {i} missing fields: {missing}")
        all_tasks_valid = False
    else:
        print(f"  ✅ Task {i} ({task_config['name']}): Valid structure")

if not all_tasks_valid:
    sys.exit(1)
print()

# Step 3: Test each grader
print(f"STEP 3: Grader Execution")
all_graders_valid = True
for i, task_config in enumerate(tasks, 1):
    try:
        env_task = DataCleaningEnv()
        env_task.load_dataframe(task_config['data'].copy())
        
        for action_name in task_config['action_sequence']:
            obs, reward, done, _ = env_task.step(Action(action_type=action_name))
            if done:
                break
        
        final_state = env_task.state()
        grader = grader_map.get(task_config['name'], grade_hard)
        raw_score = grader(final_state)
        score = safe_score(float(raw_score))
        
        # Check score is valid
        if score <= 0.0 or score >= 1.0:
            print(f"  ❌ Task {i} ({task_config['name']}): Score {score} NOT between 0 and 1")
            all_graders_valid = False
        elif not isinstance(score, (int, float)):
            print(f"  ❌ Task {i} ({task_config['name']}): Score {score} is not numeric (type: {type(score)})")
            all_graders_valid = False
        else:
            print(f"  ✅ Task {i} ({task_config['name']}): Score = {score}")
    
    except Exception as e:
        print(f"  ❌ Task {i} ({task_config['name']}): Execution failed - {str(e)}")
        all_graders_valid = False

if not all_graders_valid:
    sys.exit(1)
print()

# Step 4: Simulate /tasks endpoint response
print(f"STEP 4: Simulate /tasks Endpoint Response")
try:
    endpoint_response = {
        "tasks": [],
        "summary": {
            "total_tasks": len(tasks),
        }
    }
    
    for task_config in tasks:
        env_task = DataCleaningEnv()
        env_task.load_dataframe(task_config['data'].copy())
        
        for action_name in task_config['action_sequence']:
            obs, reward, done, _ = env_task.step(Action(action_type=action_name))
            if done:
                break
        
        final_state = env_task.state()
        grader = grader_map.get(task_config['name'], grade_hard)
        raw_score = grader(final_state)
        score = safe_score(float(raw_score))
        
        endpoint_response["tasks"].append({
            "task": task_config["task"],
            "difficulty": task_config["difficulty"],
            "score": score
        })
    
    print(f"  Response has {len(endpoint_response['tasks'])} tasks")
    for task in endpoint_response["tasks"]:
        score = task['score']
        print(f"    - {task['task']}: score={score} (valid: {0 < score < 1})")
    
    print(f"  ✅ PASS: /tasks endpoint ready")
except Exception as e:
    print(f"  ❌ FAIL: /tasks endpoint error - {str(e)}")
    sys.exit(1)
print()

# Final summary
print("=" * 70)
print("FINAL SUBMISSION READINESS CHECK")
print("=" * 70)
print(f"✅ Tasks count: {len(tasks)} (≥ 3 required)")
print(f"✅ All tasks have graders")
print(f"✅ All scores between 0 and 1")
print(f"✅ /tasks endpoint working")
print()
print("🚀 REPOSITORY IS READY FOR SUBMISSION")
print("=" * 70)
