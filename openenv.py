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


def parse_args():
    parser = argparse.ArgumentParser(description="Local OpenEnv wrapper for this repo")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Initialize a local OpenEnv project scaffold")
    init_parser.add_argument("name", help="Name of the new environment folder")

    run_parser = subparsers.add_parser("run", help="Run local tasks")
    run_parser.add_argument("target", choices=["server"], help="Target to run")

    push_parser = subparsers.add_parser("push", help="Prepare a deploy push")
    push_parser.add_argument("--repo-id", required=True, help="Repository ID for deployment (user/repo)")

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
    else:
        print("No command provided. Use --help for usage information.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
