#!/bin/bash
# Force push all changes to ensure deployment sees the latest code
cd 'c:\Users\pb168\Downloads\archive (1)\newenv'

echo "Adding critical files..."
git add pyproject.toml server/app.py app.py

echo "Committing changes..."
git commit -m "Critical: Update entry point to server.app:main with proper main() function"

echo "Pushing to GitHub..."
git push origin main

echo "Done! Changes pushed to GitHub"
