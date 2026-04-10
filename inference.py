"""
Baseline Inference Script for Data Cleaning Environment

This script demonstrates the complete data cleaning pipeline with:
- Structured output following [START], [STEP], [END] format
- OpenAI Client integration for LLM-based inference
- Reproducible random seeding
- Error handling and logging
"""

import json
import os
import sys
import logging
from typing import Dict, Any, List
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client with error handling
client = None
try:
    api_base_url = os.environ.get("API_BASE_URL")
    api_key = os.environ.get("API_KEY")
    if api_base_url and api_key:
        client = OpenAI(
            base_url=api_base_url,
            api_key=api_key
        )
    else:
        print("WARNING: API_BASE_URL and/or API_KEY not set. OpenAI features will be disabled.", file=sys.stderr)
except Exception as e:
    print(f"WARNING: Failed to initialize OpenAI client: {e}. OpenAI features will be disabled.", file=sys.stderr)
    client = None

# Import environment components
from env.environment import DataCleaningEnv
from env.models import Action
from env.graders import grade_easy, grade_medium_normalize, grade_medium_missing, grade_hard, grade_easy_normalize, grade_medium_duplicates, grade_hard_complex, safe_score
from env.tasks import get_tasks


def _proxy_post_chat_completion(final_state):
    if client is None:
        return "OpenAI client not available - cannot generate summary."
    model_name = os.environ["MODEL_NAME"]
    prompt = (
        "Summarize whether the uploaded data was cleaned correctly by following fill_missing, normalize, and remove_duplicates. "
        f"Final state: {final_state}"
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for data cleaning."},
            {"role": "user", "content": prompt},
        ],
    )
    if not response.choices:
        return ""
    return response.choices[0].message["content"].strip()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class DataCleaningInference:
    """Inference runner for Data Cleaning Environment"""
    
    def __init__(self):
        self.env = DataCleaningEnv()
        self.results = []
        self.grader_map = {
            "easy": grade_easy,
            "medium_normalize": grade_medium_normalize,
            "medium_missing": grade_medium_missing,
            "hard": grade_hard,
            "easy_normalize": grade_easy_normalize,
            "medium_duplicates": grade_medium_duplicates,
            "hard_complex": grade_hard_complex,
        }
    
    def run_single_task(self, task_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single data cleaning task with structured output.
        
        Args:
            task_config: Task configuration dictionary
        
        Returns:
            Dict with task results including score and logs
        """
        # Print task header with [START] marker
        print("[START]")
        print(f"task: {task_config['task']}")
        print()
        
        # Reset environment with task data
        self.env.load_dataframe(task_config["data"].copy())
        
        logs = []
        cleaned_state = None
        
        # Execute each action in the task sequence
        for action_name in task_config["action_sequence"]:
            # Print [STEP] marker before each action
            print("[STEP]")
            print(f"action: {action_name}")
            
            # Execute the action
            obs, reward, done, _ = self.env.step(Action(action_type=action_name))
            
            # Print reward
            print(f"reward: {reward.score}")
            print()
            
            # Log the step
            logs.append({
                "action": action_name,
                "reward": reward.score
            })
            
            cleaned_state = self.env.state()
            
            if done:
                break
        
        # Calculate final score using grader
        grader = self.grader_map.get(task_config['name'], grade_hard)
        raw_score = grader(cleaned_state)
        # FORCE SAFE SCORE
        final_score = safe_score(float(raw_score))
        
        # Print [END] marker with final score
        print("[END]")
        print(f"score: {final_score}")
        print()
        
        return {
            "task": task_config["task"],
            "difficulty": task_config.get("difficulty", "unknown"),
            "score": final_score,
            "logs": logs,
            "cleaned_state": cleaned_state
        }


def main():
    """Main entry point for inference script"""
    logger.info("Starting Data Cleaning Inference...")

    try:
        tasks = get_tasks()  # gets all 5 tasks from env/tasks.py

        for task_config in tasks:
            env = DataCleaningEnv()
            env.load_dataframe(task_config["data"].copy())

            print("[START]")
            print(f"task: {task_config['task']}")
            print()

            for action_name in task_config["action_sequence"]:
                print("[STEP]")
                print(f"action: {action_name}")
                obs, reward, done, _ = env.step(Action(action_type=action_name))
                print(f"reward: {reward.score}")
                print()
                if done:
                    break

            final_state = env.state()
            grader = DataCleaningInference().grader_map.get(task_config['name'], grade_hard)
            raw_score = grader(final_state)
            score = safe_score(float(raw_score))

            print("[END]")
            print(f"score: {score}")
            print()

            if os.environ.get("API_BASE_URL") and os.environ.get("API_KEY"):
                try:
                    llm_output = _proxy_post_chat_completion(final_state)
                    print("[LLM PROXY OUTPUT]")
                    print(llm_output)
                except Exception as exc:
                    logger.warning("LLM proxy request failed: %s", exc)

    except Exception as e:
        logger.error(f"Inference failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
