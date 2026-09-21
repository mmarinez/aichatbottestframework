import os
import sys
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import CAPTURES
from evaluators.recorder import load_captures

DEFAULT_CAPTURE_FILE = CAPTURES / "latest.jsonl"

@lru_cache(maxsize=None)
def _index(path: str) -> dict:
    """capture_id -> record, parsed  once per path"""
    return {r["capture_id"]: r for r in load_captures(Path(path))}

def call_api(prompt, options, context):
    config = options.get("config") or {}
    path = config.get("captureFile") or os.environ.get("CAPTURE_FILE") or DEFAULT_CAPTURE_FILE

    capture_id = (context.get("vars") or {}).get("capture_id")
    if not capture_id:
        return {"error": "test case has no 'capture_id' var -- check cases.json"}


    record = _index(str(path)).get(capture_id)
    if record is None:
        return {"error": f"no capture for {capture_id!r} in {path}; re-run pytest to refresh"}

    return {"output": record["response"]}