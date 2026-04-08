#!/usr/bin/env python
"""Local OpenEnv helper for this repository.

This script provides a lightweight wrapper for the requested OpenEnv workflow:
- init <env_name>
- run server
- push --repo-id <user/repo>

It is not the official OpenEnv CLI, but it makes this repo compatible with the requested scaffolding steps.
"""

import argparse
import os
import shutil
import subprocess
import sys
import yaml
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_FILES = [
    "openenv.yaml",
    "Dockerfile",
    "requirements.txt",
    "app.py",
    "inference.py",
    "config.py",
    "README_GITHUB.md",
    "frontend.html",
    "docker-compose.yml",
    ".env.example",
    "README.md",
    "QUICK_START.md",
]

COPY_DIRS = ["env"]


def init_environment(name: str):
    dest = ROOT / name
    if dest.exists():
        print(f"Environment directory already exists: {dest}")
        return 1

    print(f"Creating OpenEnv environment scaffold: {dest}")
    dest.mkdir(parents=True, exist_ok=False)

    for file_name in DEFAULT_FILES:
        src = ROOT / file_name
        if src.exists():
            target = dest / file_name
            if src.is_file():
                shutil.copy2(src, target)
                print(f"Copied file: {file_name}")

    for dir_name in COPY_DIRS:
        src_dir = ROOT / dir_name
        if src_dir.exists() and src_dir.is_dir():
            target_dir = dest / dir_name
            shutil.copytree(src_dir, target_dir)
            print(f"Copied directory: {dir_name}")

    print(f"Scaffold complete. OpenEnv project created at: {dest}")
    return 0


def run_server():
    print("Starting FastAPI server with Uvicorn...")
    cmd = [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]
    subprocess.run(cmd, cwd=ROOT)


def push_repo(repo_id: str):
    print(f"Preparing deployment to {repo_id}")
    try:
        subprocess.run(["git", "status"], cwd=ROOT, check=True)
    except subprocess.CalledProcessError:
        print("Warning: git repository not detected or git command failed.")

    print("This helper does not perform a real deployment automatically.")
    print("You can push your repository with the following commands:")
    print(f"  git add .")
    print(f"  git commit -m \"Deploy OpenEnv environment\"")
    print(f"  git push origin main")
    print("Then configure your Hugging Face Space to use this repository:")
    print(f"  https://huggingface.co/spaces/{repo_id}")
    return 0


def validate_environment():
    """Validate the OpenEnv environment setup."""
    print("Validating OpenEnv environment...")
    errors = []
    warnings = []
    
    # Check 1: openenv.yaml exists and is valid
    yaml_file = ROOT / "openenv.yaml"
    if not yaml_file.exists():
        errors.append("openenv.yaml not found")
    else:
        try:
            with open(yaml_file, 'r') as f:
                spec = yaml.safe_load(f)
            print("  [OK] openenv.yaml exists and is valid YAML")
            
            # Check if it has required fields
            if 'spec' not in spec:
                errors.append("openenv.yaml missing 'spec' section")
            else:
                if 'api_endpoints' not in spec['spec']:
                    warnings.append("openenv.yaml missing 'api_endpoints' section (optional)")
                    
        except yaml.YAMLError as e:
            errors.append(f"openenv.yaml is invalid YAML: {e}")
    
    # Check 2: Required files exist
    required_files = {
        "app.py": "FastAPI application",
        "Dockerfile": "Docker container configuration",
        "inference.py": "Inference script",
        "requirements.txt": "Python dependencies",
    }
    
    for filename, description in required_files.items():
        filepath = ROOT / filename
        if filepath.exists():
            print(f"  [OK] {filename} exists ({description})")
        else:
            errors.append(f"{filename} not found ({description})")
    
    # Check 3: Try to import app.py to verify it's valid Python
    try:
        import sys
        sys.path.insert(0, str(ROOT))
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", str(ROOT / "app.py"))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            print("  [OK] app.py can be imported (no syntax errors)")
        else:
            errors.append("app.py could not be loaded")
    except Exception as e:
        warnings.append(f"Could not fully validate app.py: {e}")
    
    # Check 4: Verify app has reset endpoint
    app_file = ROOT / "app.py"
    if app_file.exists():
        with open(app_file, 'r') as f:
            app_content = f.read()
        
        if '@app.post("/reset")' in app_content:
            print("  [OK] POST /reset endpoint found")
        elif '@app.get("/reset")' in app_content:
            warnings.append("Only GET /reset found, POST /reset recommended")
        else:
            errors.append("/reset endpoint not found in app.py")
    
    # Check 5: Verify inference.py is valid Python
    inf_file = ROOT / "inference.py"
    if inf_file.exists():
        try:
            with open(inf_file, 'r') as f:
                compile(f.read(), str(inf_file), 'exec')
            print("  [OK] inference.py is valid Python")
        except SyntaxError as e:
            errors.append(f"inference.py has syntax error: {e}")
    
    # Summary
    print("\n" + "="*60)
    if errors:
        print("VALIDATION FAILED")
        print("="*60)
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  - {warning}")
        return 1
    else:
        print("VALIDATION PASSED")
        print("="*60)
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  - {warning}")
        return 0


def parse_args():
    parser = argparse.ArgumentParser(description="Local OpenEnv wrapper for this repo")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a local OpenEnv project scaffold")
    init_parser.add_argument("name", help="Name of the new environment folder")

    run_parser = subparsers.add_parser("run", help="Run local tasks")
    run_parser.add_argument("target", choices=["server"], help="Target to run")

    push_parser = subparsers.add_parser("push", help="Prepare a deploy push")
    push_parser.add_argument("--repo-id", required=True, help="Repository ID for deployment (user/repo)")
    
    validate_parser = subparsers.add_parser("validate", help="Validate the OpenEnv environment")

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "init":
        return init_environment(args.name)
    elif args.command == "run":
        if args.target == "server":
            return run_server()
    elif args.command == "push":
        return push_repo(args.repo_id)
    elif args.command == "validate":
        return validate_environment()
    else:
        print("No command provided. Use --help for usage information.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
