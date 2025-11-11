"""Application configuration."""

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # API Settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DOCUMENTS_DIR: Path = BASE_DIR / "documents"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    EXPORTS_DIR: Path = BASE_DIR / "exports"
    IMAGES_DIR: Path = BASE_DIR / "images"

    # Calculation Engine Settings
    CALC_TIMEOUT: int = 30  # seconds
    MAX_CALC_MEMORY: int = 512  # MB (not enforced in MVP)

    # Export Settings
    PANDOC_PATH: str = "pandoc"  # Use system pandoc
    PDF_ENGINE: str = "pdflatex"  # or xelatex, lualatex

    # Template Settings
    TEMPLATE_VARIABLES_PATTERN: str = r"\{\{(\w+)\}\}"

    # Future LLM Settings (not used in MVP)
    LLM_ENABLED: bool = False
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LOCAL_LLM_ENDPOINT: str = "http://localhost:11434/v1"


settings = Settings()
