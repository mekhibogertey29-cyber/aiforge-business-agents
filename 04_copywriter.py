"""
OWNED JOB: Write the full product title, description, bullet points and tags.
Never touch design assets or pricing.
"""
from agents.base_agent import BaseAgent
from datetime import datetime

class Copywriter(BaseAgent):
    def __init__(self):
        super().__init__(
            name="04_copywriter",
            owned_job="Write the full product title, description, bullet points and tags. Never touch design assets or pricing.",
            output_file="copy.json"
        )

    def run(self):
        self._set_status("working", "Writing sales copy")
        spec = self.read_input("product_spec.json")
        if not spec:
            self._set_status("error", "No product_spec.json")
            return

        title = f"{spec['title']} | Instant Download"
        description = f"""Transform your workflow with this premium {spec['niche']} package.

Perfect for creators, entrepreneurs and busy professionals who want results without the overwhelm.

What you get:
- High-quality ready-to-use files
- Instant access after purchase
- Commercial-friendly license included

Created by {spec.get('agent', 'AIForge')} for real-world use."""

        bullets = [
            "Instant digital download – start using in minutes",
            "Professionally designed and tested",
            "Includes bonus materials",
            "Lifetime updates when available",
            "Simple license for personal & commercial use"
        ]

        tags = [spec["niche"].replace(" ", "-"), "digital-download", "instant", "printable", "productivity"]

        payload = {
            "product_id": spec["product_id"],
            "title": title,
            "description": description,
            "bullets": bullets,
            "tags": tags,
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(payload, is_json=True)
        self.log(f"Copy written for {title}")
        return payload

if __name__ == "__main__":
    Copywriter().run()