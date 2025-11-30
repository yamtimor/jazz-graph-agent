from pathlib import Path
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    llm_model: str = os.getenv("LLM_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "3000"))
    
    # API Keys (provider-specific)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")

    # Data source
    jazz_disco_base_url: str = "https://www.jazzdisco.org"

    # Output
    output_html_path: Path = OUTPUT_DIR / "jazz_graph.html"
    output_metrics_path: Path = OUTPUT_DIR / "metrics.json"


CONFIG = JazzGraphConfig()
