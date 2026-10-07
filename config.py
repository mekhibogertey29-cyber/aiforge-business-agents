# Business Agents Config - Isolated Multi-Agent System
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"
AGENTS_DIR = BASE_DIR / "agents"

# Ensure dirs
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Business settings
BUSINESS_NAME = "AIForge Products"
OWNER = "You"
CURRENCY = "USD"

# Simulation mode (True = safe paper/demo, no real money/API keys needed)
SIMULATION_MODE = True

# LLM settings (user fills real keys later)
LLM_PROVIDER = "openai"  # openai | anthropic | xai | ollama
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Product niches to cycle (digital-first for speed + real sellability)
NICHES = [
    "printable planners & trackers",
    "AI-generated digital art packs",
    "niche ebooks (productivity, side hustles)",
    "custom SVG sticker bundles",
    "Notion templates",
    "stock photo packs (AI)",
    "mini online courses (text + images)",
]

# Agent order (strict isolation - one job each)
AGENT_ORDER = [
    "01_ideator",
    "02_researcher",
    "03_designer",
    "04_copywriter",
    "05_lister",
    "06_marketer",
    "07_sales_tracker",
    "08_optimizer",
]