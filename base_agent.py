"""
Base for every isolated agent.
Rule: one owned job, one private output file, zero shared mutable state.
"""
from pathlib import Path
import json
from datetime import datetime
from config import OUTPUT_DIR, DATA_DIR, SIMULATION_MODE, BUSINESS_NAME

class BaseAgent:
    def __init__(self, name: str, owned_job: str, output_file: str):
        self.name = name
        self.owned_job = owned_job
        self.output_path = OUTPUT_DIR / output_file
        self.status_path = DATA_DIR / f"{name}_status.json"
        self._set_status("idle", "Waiting")

    def _set_status(self, state: str, task: str, extra: dict = None):
        status = {
            "agent": self.name,
            "state": state,          # idle | working | done | error
            "current_task": task,
            "owned_job": self.owned_job,
            "last_update": datetime.utcnow().isoformat() + "Z",
            "extra": extra or {}
        }
        self.status_path.write_text(json.dumps(status, indent=2))

    def read_input(self, filename: str):
        """Only read what is explicitly allowed."""
        path = OUTPUT_DIR / filename
        if not path.exists():
            return None
        if filename.endswith(".json"):
            return json.loads(path.read_text())
        return path.read_text()

    def write_output(self, content, is_json=False):
        """Write ONLY to own file."""
        if is_json:
            self.output_path.write_text(json.dumps(content, indent=2))
        else:
            self.output_path.write_text(str(content))
        self._set_status("done", f"Wrote {self.output_path.name}")

    def log(self, msg: str):
        print(f"[{self.name}] {msg}")

    def run(self):
        raise NotImplementedError("Each agent must implement its single owned job")