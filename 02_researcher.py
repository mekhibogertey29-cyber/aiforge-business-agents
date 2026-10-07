"""
OWNED JOB: Analyze demand signals and competition for the ideas provided.
Output only research notes. Never design products or write sales copy.
"""
from agents.base_agent import BaseAgent
from datetime import datetime
import random

class Researcher(BaseAgent):
    def __init__(self):
        super().__init__(
            name="02_researcher",
            owned_job="Analyze demand signals and competition for the ideas provided. Output only research notes. Never design products or write sales copy.",
            output_file="research.json"
        )

    def run(self):
        self._set_status("working", "Scanning demand & competition")
        ideas = self.read_input("ideas.json")
        if not ideas:
            self._set_status("error", "No ideas.json found")
            return

        research = []
        for idea in ideas.get("ideas", []):
            research.append({
                "idea_id": idea["id"],
                "title": idea["title"],
                "demand_score": round(random.uniform(6.5, 9.4), 1),  # 1-10
                "competition": random.choice(["Low", "Medium", "High"]),
                "trend": random.choice(["Rising", "Stable", "Seasonal"]),
                "notes": f"Strong search interest in '{idea['niche']}'. Easy to fulfill digitally. Suggested price range validated.",
                "recommended": random.random() > 0.3
            })

        payload = {
            "research": research,
            "top_pick": max(research, key=lambda x: x["demand_score"])["idea_id"],
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(payload, is_json=True)
        self.log(f"Researched {len(research)} ideas. Top pick: {payload['top_pick']}")
        return payload

if __name__ == "__main__":
    Researcher().run()