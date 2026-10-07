"""
OWNED JOB (single sentence): Generate 3 high-potential digital product ideas 
for the current niche. Never research market size or write copy.
"""
import random
from datetime import datetime
from agents.base_agent import BaseAgent
from config import NICHES, BUSINESS_NAME

class Ideator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="01_ideator",
            owned_job="Generate 3 high-potential digital product ideas for the current niche. Never research market size or write copy.",
            output_file="ideas.json"
        )

    def run(self):
        self._set_status("working", "Brainstorming product ideas")
        niche = random.choice(NICHES)
        # Lightweight idea generation (replace with LLM call later)
        ideas = [
            {
                "id": f"idea_{i+1}",
                "title": f"{niche.title()} – Premium Pack #{i+1}",
                "niche": niche,
                "type": "digital",
                "price_suggestion": round(random.uniform(9.99, 47.00), 2),
                "description_seed": f"Complete ready-to-sell {niche} package with AI-assisted assets.",
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            for i in range(3)
        ]
        payload = {
            "business": BUSINESS_NAME,
            "selected_niche": niche,
            "ideas": ideas,
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(payload, is_json=True)
        self.log(f"Generated 3 ideas in niche: {niche}")
        return payload

if __name__ == "__main__":
    Ideator().run()