"""
OWNED JOB: Create product specifications and asset list for the top researched idea.
Never write marketing copy or set prices.
"""
from agents.base_agent import BaseAgent
from datetime import datetime
import random

class Designer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="03_designer",
            owned_job="Create product specifications and asset list for the top researched idea. Never write marketing copy or set prices.",
            output_file="product_spec.json"
        )

    def run(self):
        self._set_status("working", "Designing product package")
        research = self.read_input("research.json")
        ideas = self.read_input("ideas.json")
        if not research or not ideas:
            self._set_status("error", "Missing upstream files")
            return

        top_id = research["top_pick"]
        top_idea = next(i for i in ideas["ideas"] if i["id"] == top_id)

        # Simulated product package (digital)
        assets = [
            {"name": "Main PDF / Digital File", "format": "PDF", "pages": random.randint(15, 60)},
            {"name": "Bonus Checklist", "format": "PDF", "pages": 2},
            {"name": "Cover Image", "format": "PNG", "size": "2000x2000"},
            {"name": "Mockup Pack", "format": "PNG", "count": 5},
            {"name": "License & Instructions", "format": "TXT", "pages": 1},
        ]

        spec = {
            "product_id": f"prod_{top_id}",
            "title": top_idea["title"],
            "niche": top_idea["niche"],
            "type": "digital_download",
            "assets": assets,
            "fulfillment": "instant_download",
            "estimated_cost": 0.0,  # pure digital
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(spec, is_json=True)
        self.log(f"Designed package for: {spec['title']}")
        return spec

if __name__ == "__main__":
    Designer().run()