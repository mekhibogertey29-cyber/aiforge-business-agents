"""
OWNED JOB: Suggest concrete improvements based on sales data and research.
Never implement changes itself.
"""
from agents.base_agent import BaseAgent
from datetime import datetime

class Optimizer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="08_optimizer",
            owned_job="Suggest concrete improvements based on sales data and research. Never implement changes itself.",
            output_file="optimizations.md"
        )

    def run(self):
        self._set_status("working", "Analyzing performance & suggesting upgrades")
        sales = self.read_input("sales.json")
        research = self.read_input("research.json")
        listing = self.read_input("listing.json")

        if not sales:
            self._set_status("error", "No sales data")
            return

        rev = sales["last_30_days"]["revenue"]
        units = sales["last_30_days"]["units"]

        suggestions = []
        if units < 5:
            suggestions.append("- Price test: drop 15-20% for 7 days and measure conversion.")
            suggestions.append("- Add a free sample / lead magnet to the listing.")
        if rev > 100:
            suggestions.append("- Create a higher-ticket bundle version (+$29-49).")
            suggestions.append("- Spin a second product in the same niche.")
        suggestions.append("- Refresh cover image and first 3 bullets every 14 days.")
        suggestions.append("- Double down on the highest-reach free channel from marketing plan.")
        suggestions.append("- Collect 3 real customer quotes and add as social proof.")

        md = f"""# Optimization Report – {listing.get('title', 'Product') if listing else 'N/A'}

**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC  
**Agent:** {self.name}

## Current Snapshot
- Units (30d): {units}
- Revenue (30d): ${rev}
- Avg daily units: {sales['last_30_days']['avg_daily_units']}

## Recommended Actions (do not auto-apply)
"""
        for s in suggestions:
            md += f"{s}\n"

        md += f"""
## Next Cycle Priority
Focus on the single highest-leverage item above. Re-run the full agent chain after changes.

---
Isolated output. No other files were modified.
"""
        self.write_output(md)
        self.log("Optimization suggestions written")
        return md

if __name__ == "__main__":
    Optimizer().run()