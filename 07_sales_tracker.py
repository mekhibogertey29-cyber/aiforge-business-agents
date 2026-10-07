"""
OWNED JOB: Simulate / track sales, revenue, and basic metrics for the listing.
Never change product or marketing.
"""
from agents.base_agent import BaseAgent
from datetime import datetime, timedelta
import random
import json
from pathlib import Path
from config import DATA_DIR

class SalesTracker(BaseAgent):
    def __init__(self):
        super().__init__(
            name="07_sales_tracker",
            owned_job="Simulate / track sales, revenue, and basic metrics for the listing. Never change product or marketing.",
            output_file="sales.json"
        )

    def run(self):
        self._set_status("working", "Updating sales & revenue")
        listing = self.read_input("listing.json")
        if not listing:
            self._set_status("error", "No listing")
            return

        # Persistent simple sales log
        log_path = DATA_DIR / "sales_log.json"
        if log_path.exists():
            history = json.loads(log_path.read_text())
        else:
            history = []

        # Simulate some daily sales (realistic digital product curve)
        today_sales = random.randint(0, 7)
        revenue = round(today_sales * listing["price"], 2)
        entry = {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "listing_id": listing["listing_id"],
            "units": today_sales,
            "revenue": revenue,
            "price": listing["price"]
        }
        history.append(entry)
        # Keep last 30 days
        history = history[-30:]
        log_path.write_text(json.dumps(history, indent=2))

        total_units = sum(h["units"] for h in history)
        total_revenue = round(sum(h["revenue"] for h in history), 2)

        payload = {
            "listing_id": listing["listing_id"],
            "today": entry,
            "last_30_days": {
                "units": total_units,
                "revenue": total_revenue,
                "avg_daily_units": round(total_units / max(len(history), 1), 2)
            },
            "history": history,
            "agent": self.name,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.write_output(payload, is_json=True)
        self.log(f"Today: {today_sales} units | ${revenue} | Total: ${total_revenue}")
        return payload

if __name__ == "__main__":
    SalesTracker().run()