import json
from env.environment import DataCleaningEnv
from env.models import Action
from env.tasks import get_tasks
from env.graders import grade_easy, grade_medium_normalize, grade_medium_missing, grade_hard, grade_easy_normalize, grade_medium_duplicates, grade_hard_complex


def run_task(task_config):
    """Run a single task and return score, cleaned state, and logs"""
    env = DataCleaningEnv()
    env.load_dataframe(task_config["data"].copy())
    cleaned_state = None
    
    grader_map = {
        "easy": grade_easy,
        "medium_normalize": grade_medium_normalize,
        "medium_missing": grade_medium_missing,
        "hard": grade_hard,
        "easy_normalize": grade_easy_normalize,
        "medium_duplicates": grade_medium_duplicates,
        "hard_complex": grade_hard_complex,
    }
    
    logs = []
    print(f"\n{'='*60}")
    print(f"TASK: {task_config['task'].upper()}")
    print(f"Difficulty: {task_config['difficulty'].upper()}")
    print(f"{'='*60}")
    print("[START]")
    print(f"task: {task_config['task']}")
    print()

    for action_name in task_config["action_sequence"]:
        obs, reward, done, _ = env.step(Action(action_type=action_name))
        print("[STEP]")
        print(f"action: {action_name}")
        print(f"reward: {reward.score}")
        print()
        logs.append({"action": action_name, "reward": reward.score})
        cleaned_state = env.state()
        if done:
            break

    grader = grader_map.get(task_config['name'], grade_hard)
    score = grader(cleaned_state)
    print("[END]")
    print(f"score: {score}")
    print()
    
    return {
        "task": task_config["task"],
        "difficulty": task_config["difficulty"],
        "score": score,
        "logs": logs,
        "cleaned_state": cleaned_state
    }


def run_all_tasks():
    """Run all tasks and show difficulty variation"""
    tasks = get_tasks()
    results = []
    scores_by_difficulty = {
        "easy": [],
        "medium": [],
        "hard": []
    }

    for task_config in tasks:
        result = run_task(task_config)
        results.append(result)
        difficulty = task_config["difficulty"]
        scores_by_difficulty[difficulty].append(result["score"])

    # Summary Report
    print("\n" + "="*60)
    print("FINAL SUMMARY REPORT")
    print("="*60)
    
    for difficulty in ["easy", "medium", "hard"]:
        scores = scores_by_difficulty[difficulty]
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"\n{difficulty.upper()} Tasks:")
            print(f"  Count: {len(scores)}")
            print(f"  Scores: {scores}")
            print(f"  Average: {avg_score:.2f}")
    
    overall_avg = sum(r["score"] for r in results) / len(results) if results else 0
    print(f"\nOverall Average Score: {overall_avg:.2f}")
    print(f"Total Tasks Run: {len(results)}")
    print(f"Score Variation: {max(r['score'] for r in results) - min(r['score'] for r in results):.2f}")
    print("="*60)

    return results


if __name__ == "__main__":
    run_all_tasks()
