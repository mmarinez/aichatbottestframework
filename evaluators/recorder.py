import json
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

def load_captures(path: Path) -> list[dict]:
    """Read a capture file. A module function, not a method"""
    if not path.exists():
        return[]
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

class Recorder:
    def __init__(self, path: Path): 
        self.path = path
        self.run_id = uuid4().hex[:8]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")

    def record(self, capture_id, prompt, response, model, duration_ms, test_id) -> None:
        entry = {
            "capture_id": capture_id,
            "run_id": self.run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "test_id": test_id,
            "model": model,
            "duration_ms": duration_ms,
            "prompt": prompt,
            "response": response,
        } 
        with self.path.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
    def export_cases(self, dest: Path): 
        """Derive the promptfoo dataset from the captures."""
        cases = [
            {"vars": {"capture_id": r["capture_id"],"prompt": r["prompt"]}}
            for r in load_captures(self.path)
        ]