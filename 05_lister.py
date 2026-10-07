"""
OWNED JOB: Assemble the final listing package (price, platform targets, files list).
Never market or track sales.
"""
from agents.base_agent import BaseAgent
from datetime import datetime
import random

class Lister(BaseAgent):
    def __init__(self):
        super().__init__(
            name="05_lister",
            owned_job="Assemble the final listing package (price, platform targets, files list). Never market or track sales.",
            output_file="listing.json"
        )

    def run(self):
        self._set_status("working", "Building listing")
        spec = self.read_input("product_spec.json")
        copy = self.read_input("copy.json")
        ideas = self.read_input("ideas.json")
        if not all([spec, copy, ideas]):
            self._set_status("error", "Missing upstream")
            return

        # Find original price suggestion
        idea = next((i for i in ideas["ideas"] if i["id"] in spec["product_id"]), ideas["ideas"][0])
        price = idea.get("price_suggestion", 19.99)

        listing = {
            "listing_id": f"list_{spec['product_id']}",
            "product_id": spec["product_id"],
            "title": copy["title"],
            "description": copy["description"],
            "bullets": copy["bullets"],
            "tags": copy["tags"],
            "price": price,
            "currency": "USD",
            "platforms": ["Gumroad", "Etsy", "Own Store (Shopify/Stan)"],
            "status": "ready_to_publish",
            "assets": spec["assets"],
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(listing, is_json=True)
        self.log(f"Listing ready @ ${price}")
        return listing

if __name__ == "__main__":
    Lister().run()