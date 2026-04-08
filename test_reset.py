
import sys
import os
work_dir = r"c:\Users\pb168\Downloads\archive (1)\newenv"
sys.path.insert(0, work_dir)
os.chdir(work_dir)

from app import api_reset_post
result = api_reset_post()
print(f"DIRECT CALL Result: {type(result)}", file=sys.stderr)
print(f"DIRECT CALL Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}", file=sys.stderr)
print(f"DIRECT CALL Value: {result}", file=sys.stderr)
