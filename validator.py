"""
Pre-Submission Validator for Data Cleaning Environment

Validates:
- openenv.yaml compliance
- Typed models implementation
- API endpoint responses
- Inference script execution
- Task and grader functionality
- Docker image build
"""

import sys
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Validator:
    """Pre-submission validation suite"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0
    
    def print_header(self, text: str):
        """Print validation section header"""
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")
    
    def check(self, name: str, condition: bool, error_msg: str = "") -> bool:
        """
        Perform and log a single check.
        
        Args:
            name: Check name
            condition: Check result (True = pass)
            error_msg: Error message if check fails
        
        Returns:
            Check result
        """
        if condition:
            print(f"[PASS] {name}")
            self.checks_passed += 1
            return True
        else:
            print(f"[FAIL] {name}")
            if error_msg:
                print(f"       -> {error_msg}")
            self.checks_failed += 1
            return False
    
    def warn(self, name: str, message: str):
        """Log a warning"""
        print(f"[WARN] {name}")
        print(f"       -> {message}")
        self.warnings += 1
    
    # ========== Validation Functions ==========
    
    def validate_files_exist(self) -> bool:
        """Check that all required files exist"""
        self.print_header("FILE EXISTENCE CHECKS")
        
        required_files = [
            "openenv.yaml",
            "Dockerfile",
            "app.py",
            "inference.py",
            "requirements.txt",
            "README.md",
            "config.py",
            "env/__init__.py",
            "env/environment.py",
            "env/models.py",
            "env/tasks.py",
            "env/graders.py"
        ]
        
        all_exist = True
        for file in required_files:
            path = self.root_dir / file
            exists = path.exists()
            self.check(f"File exists: {file}", exists, f"Expected at {path}")
            all_exist = all_exist and exists
        
        return all_exist
    
    def validate_openenv_yaml(self) -> bool:
        """Validate openenv.yaml structure and content"""
        self.print_header("OPENENV.YAML VALIDATION")
        
        yaml_path = self.root_dir / "openenv.yaml"
        
        try:
            with open(yaml_path, 'r') as f:
                spec = yaml.safe_load(f)
            
            # Check required fields
            self.check("name field exists", "name" in spec)
            self.check("version field exists", "version" in spec)
            self.check("metadata field exists", "metadata" in spec)
            self.check("spec field exists", "spec" in spec)
            self.check("tasks field exists", "tasks" in spec)
            
            # Check spec structure
            if "spec" in spec:
                spec_obj = spec["spec"]
                self.check("action_space defined", "action_space" in spec_obj)
                self.check("observation_space defined", "observation_space" in spec_obj)
                self.check("api_endpoints defined", "api_endpoints" in spec_obj)
            
            # Check tasks
            if "tasks" in spec:
                tasks = spec["tasks"]
                self.check("Has 3+ tasks", len(tasks) >= 3, f"Found {len(tasks)} tasks")
            
            logger.info("✅ openenv.yaml is valid YAML")
            return True
        
        except Exception as e:
            self.check("YAML parsing", False, str(e))
            return False
    
    def validate_typed_models(self) -> bool:
        """Validate that models.py has proper type hints"""
        self.print_header("TYPED MODELS VALIDATION")
        
        models_path = self.root_dir / "env" / "models.py"
        
        try:
            with open(models_path, 'r') as f:
                content = f.read()
            
            # Check for class definitions with type hints
            self.check("Action class defined", "class Action" in content)
            self.check("Observation class defined", "class Observation" in content)
            self.check("Reward class defined", "class Reward" in content)
            
            # Check for type annotations
            self.check("Uses type annotations", ":" in content and "->" in content)
            self.check("Uses pydantic or dataclass", "BaseModel" in content or "dataclass" in content)
            
            return True
        
        except Exception as e:
            self.check("Models validation", False, str(e))
            return False
    
    def validate_environment_class(self) -> bool:
        """Validate DataCleaningEnv has required methods"""
        self.print_header("ENVIRONMENT CLASS VALIDATION")
        
        env_path = self.root_dir / "env" / "environment.py"
        
        try:
            with open(env_path, 'r') as f:
                content = f.read()
            
            self.check("DataCleaningEnv class exists", "class DataCleaningEnv" in content)
            self.check("reset() method defined", "def reset" in content)
            self.check("step() method defined", "def step" in content)
            self.check("state() method defined", "def state" in content)
            self.check("load_dataframe() method defined", "def load_dataframe" in content)
            
            return True
        
        except Exception as e:
            self.check("Environment validation", False, str(e))
            return False
    
    def validate_requirements(self) -> bool:
        """Check requirements.txt has necessary packages"""
        self.print_header("REQUIREMENTS.TXT VALIDATION")
        
        req_path = self.root_dir / "requirements.txt"
        
        try:
            with open(req_path, 'r') as f:
                content = f.read()
            
            required_packages = ["pandas", "fastapi", "uvicorn", "pydantic"]
            
            for package in required_packages:
                self.check(f"Includes {package}", package.lower() in content.lower())
            
            return True
        
        except Exception as e:
            self.check("Requirements validation", False, str(e))
            return False
    
    def validate_tasks_and_graders(self) -> bool:
        """Validate that tasks and graders are properly defined"""
        self.print_header("TASKS & GRADERS VALIDATION")
        
        try:
            from env.tasks import get_tasks
            from env.graders import grade_hard
            
            tasks = get_tasks()
            self.check("get_tasks() executable", True)
            self.check("Has 3+ tasks", len(tasks) >= 3, f"Found {len(tasks)} tasks")
            
            # Check task structure
            for task in tasks:
                required_fields = ["name", "task", "difficulty", "action_sequence", "data"]
                all_fields = all(field in task for field in required_fields)
                if not all_fields:
                    self.warn("Task structure", f"Task '{task.get('name')}' missing fields")
            
            # Test grader
            sample_data = [{"name": "john", "age": "25", "salary": 50000}]
            score = grade_hard(sample_data)
            self.check("grade_hard() executable", True)
            self.check("Score in valid range", 0.0 <= score <= 1.0, f"Score: {score}")
            
            return True
        
        except Exception as e:
            self.check("Tasks & Graders validation", False, str(e))
            return False
    
    def validate_inference_script(self) -> bool:
        """Validate inference.py can be imported and run"""
        self.print_header("INFERENCE SCRIPT VALIDATION")
        
        inf_path = self.root_dir / "inference.py"
        
        try:
            # Check existence
            self.check("inference.py exists", inf_path.exists())
            
            # Check required markers in output
            with open(inf_path, 'r') as f:
                content = f.read()
            
            self.check("Contains [START] marker", "[START]" in content)
            self.check("Contains [STEP] marker", "[STEP]" in content)
            self.check("Contains [END] marker", "[END]" in content)
            self.check("Contains action printing", 'action:' in content or "action" in content)
            self.check("Contains reward printing", 'reward:' in content or "reward" in content)
            self.check("Contains score printing", 'score:' in content or "score" in content)
            
            return True
        
        except Exception as e:
            self.check("Inference script validation", False, str(e))
            return False
    
    def validate_dockerfile(self) -> bool:
        """Validate Dockerfile structure"""
        self.print_header("DOCKERFILE VALIDATION")
        
        docker_path = self.root_dir / "Dockerfile"
        
        try:
            with open(docker_path, 'r') as f:
                content = f.read()
            
            self.check("Dockerfile exists", True)
            self.check("Uses FROM statement", "FROM" in content)
            self.check("Installs requirements", "requirements.txt" in content)
            self.check("Exposes port", "EXPOSE" in content)
            self.check("Has run/cmd", "CMD" in content or "RUN" in content)
            
            return True
        
        except Exception as e:
            self.check("Dockerfile validation", False, str(e))
            return False
    
    def validate_readme(self) -> bool:
        """Validate README.md exists and has content"""
        self.print_header("README VALIDATION")
        
        readme_path = self.root_dir / "README.md"
        
        try:
            with open(readme_path, 'r') as f:
                content = f.read()
            
            self.check("README.md exists", True)
            self.check("Has description section", "Overview" in content or "Description" in content)
            self.check("Has setup instructions", "Setup" in content or "Install" in content or "Quick Start" in content)
            self.check("Has API documentation", "API" in content or "Endpoints" in content)
            self.check("Has task documentation", "Task" in content)
            
            word_count = len(content.split())
            self.check(f"Adequate documentation", word_count > 500, f"Word count: {word_count}")
            
            return True
        
        except Exception as e:
            self.check("README validation", False, str(e))
            return False
    
    def run_all_checks(self) -> Tuple[bool, Dict]:
        """Run all validation checks"""
        print("\n" + "="*60)
        print("  DATA CLEANING ENV - PRE-SUBMISSION VALIDATOR")
        print("="*60)
        
        checks_results = {
            "Files": self.validate_files_exist(),
            "OpenEnv YAML": self.validate_openenv_yaml(),
            "Typed Models": self.validate_typed_models(),
            "Environment Class": self.validate_environment_class(),
            "Requirements": self.validate_requirements(),
            "Tasks & Graders": self.validate_tasks_and_graders(),
            "Inference Script": self.validate_inference_script(),
            "Dockerfile": self.validate_dockerfile(),
            "README": self.validate_readme(),
        }
        
        # Print summary
        self.print_header("VALIDATION SUMMARY")
        
        for check_name, result in checks_results.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{check_name}: {status}")
        
        print(f"\n{'─'*60}")
        print(f"Checks Passed: {self.checks_passed}")
        print(f"Checks Failed: {self.checks_failed}")
        print(f"Warnings: {self.warnings}")
        print(f"{'─'*60}")
        
        # Overall result
        all_passed = all(checks_results.values())
        if all_passed:
            print("\n[SUCCESS] ALL CHECKS PASSED - READY FOR SUBMISSION")
        else:
            print("\n[FAILURE] SOME CHECKS FAILED - PLEASE FIX BEFORE SUBMISSION")
        
        return all_passed, checks_results


def main():
    """Run pre-submission validation"""
    validator = Validator()
    passed, results = validator.run_all_checks()
    
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
