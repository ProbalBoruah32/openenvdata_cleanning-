from fastapi import FastAPI

app = FastAPI(title="Data Cleaning OpenEnv", description="OpenEnv compliant data cleaning environment")

@app.get("/")
def read_root():
    return {"message": "Data Cleaning OpenEnv Environment", "status": "running"}

@app.get("/reset")
def reset():
    return {
        "observation": {
            "data": [{"name": "test", "value": 1}],
            "step_count": 0
        },
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: dict):
    return {
        "observation": {
            "data": [{"name": "test", "value": 1}],
            "step_count": 1
        },
        "reward": 0.3,
        "done": False,
        "info": {}
    }

@app.get("/state")
def state():
    return {
        "observation": {
            "data": [{"name": "test", "value": 1}],
            "step_count": 0
        }
    }

@app.get("/tasks")
def tasks():
    return {
        "tasks": [
            {
                "name": "test_task",
                "difficulty": "easy",
                "score": 0.8
            }
        ],
        "summary": {
            "total_tasks": 1,
            "overall_average_score": 0.8,
            "score_variation": 0.0,
            "by_difficulty": {
                "easy": {"count": 1, "average": 0.8, "scores": [0.8]}
            }
        }
    }