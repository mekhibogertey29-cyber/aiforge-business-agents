"""
OWNED JOB: Create launch plan and promotional assets list only.
Never change the product or track revenue.
"""
from agents.base_agent import BaseAgent
from datetime import datetime, timedelta
import random

class Marketer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="06_marketer",
            owned_job="Create launch plan and promotional assets list only. Never change the product or track revenue.",
            output_file="marketing.json"
        )

    def run(self):
        self._set_status("working", "Building launch plan")
        listing = self.read_input("listing.json")
        if not listing:
            self._set_status("error", "No listing.json")
            return

        plan = {
            "listing_id": listing["listing_id"],
            "channels": [
                {"name": "Twitter/X organic", "budget": 0, "expected_reach": random.randint(500, 3000)},
                {"name": "Pinterest pins", "budget": 0, "expected_reach": random.randint(1000, 8000)},
                {"name": "Reddit value posts", "budget": 0, "expected_reach": random.randint(200, 1500)},
                {"name": "Email list (if any)", "budget": 0, "expected_reach": random.randint(50, 400)},
            ],
            "content_calendar": [
                {"day": 1, "action": "Soft launch post + free sample"},
                {"day": 2, "action": "Behind-the-scenes / how it was made"},
                {"day": 3, "action": "Customer pain → solution story"},
                {"day": 5, "action": "Limited-time bonus reminder"},
            ],
            "promo_assets_needed": [
                "3 social graphics",
                "1 short video script (15s)",
                "Email subject lines x5",
                "Pin descriptions x10"
            ],
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(plan, is_json=True)
        self.log("Launch plan created")
        return plan

if __name__ == "__main__":
    Marketer().run()