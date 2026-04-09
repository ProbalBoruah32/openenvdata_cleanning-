#!/usr/bin/env python3
"""
Test script to verify /tasks endpoint scores are valid
"""
from env.tasks import get_tasks
from env.environment import DataCleaningEnv
from env.models import Action
from env.graders import (
    grade_easy, grade_medium_normalize, grade_medium_missing, grade_hard,
    grade_easy_normalize, grade_medium_duplicates, grade_hard_complex, safe_score
)

grader_map = {
    'easy': grade_easy,
    'medium_normalize': grade_medium_normalize,
    'medium_missing': grade_medium_missing,
    'hard': grade_hard,
    'easy_normalize': grade_easy_normalize,
    'medium_duplicates': grade_medium_duplicates,
    'hard_complex': grade_hard_complex,
}

def test_tasks_endpoint():
    """Test that /tasks endpoint returns valid scores"""
    tasks = get_tasks()
    print(f'Total tasks: {len(tasks)}')
    print()
    
    if len(tasks) < 3:
        print(f'❌ FAIL: Only {len(tasks)} tasks, need at least 3')
        return False
    
    all_valid = True
    for task_config in tasks:
        env_task = DataCleaningEnv()
        env_task.load_dataframe(task_config['data'].copy())
        logs = []
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
            print(f'❌ FAIL - TASK: {task_config["task"]} SCORE: {score} (NOT between 0 and 1)')
            all_valid = False
        else:
            print(f'✅ PASS - TASK: {task_config["task"]} SCORE: {score}')
    
    print()
    if all_valid and len(tasks) >= 3:
        print('✅ ALL CHECKS PASSED - Ready for submission')
        return True
    else:
        print('❌ VALIDATION FAILED')
        return False

if __name__ == '__main__':
    success = test_tasks_endpoint()
    exit(0 if success else 1)
