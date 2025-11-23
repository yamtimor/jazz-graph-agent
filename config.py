from pathlib import Path
from dataclasses import dataclass
import os

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output"

# Make sure folders exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class JazzGraphConfig:
    # Core domain config
    seed_musician: str = "Charlie Parker"
    era_start_year: int = 1940
    era_end_year: int = 1960

    # Agent / LLM config
    llm_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    max_tokens: int = 3000

    # Data source
    jazz_disco_base_url: str = "https://www.jazzdisco.org"

    # Output
    output_html_path: Path = OUTPUT_DIR / "jazz_graph.html"
    output_metrics_path: Path = OUTPUT_DIR / "metrics.json"


CONFIG = JazzGraphConfig()
