#!/usr/bin/env python3
"""
Orchestrator – the only component allowed to call agents in sequence.
Each agent still owns exactly one job and one output file.
"""
import os
import subprocess
import sys
from pathlib import Path
from config import AGENT_ORDER, BASE_DIR

def run_agent(agent_name: str):
    script = BASE_DIR / "agents" / f"{agent_name}.py"
    if not script.exists():
        print(f"Missing: {script}")
        return False
    print(f"\n▶ Running {agent_name} ...")
    env = dict(**os.environ)
    env["PYTHONPATH"] = str(BASE_DIR)
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(BASE_DIR),
        env=env
    )
    return result.returncode == 0

def main():
    print("=" * 50)
    print("  AIForge Business Agents – Isolated Run")
    print("=" * 50)
    success = 0
    for agent in AGENT_ORDER:
        if run_agent(agent):
            success += 1
        else:
            print(f"✗ {agent} failed – stopping chain")
            break
    print(f"\nFinished {success}/{len(AGENT_ORDER)} agents.")
    print("Open the dashboard to inspect every section:")
    print("  streamlit run dashboard/app.py")

if __name__ == "__main__":
    main()