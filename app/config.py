import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Settings:
    """Container for runtime configuration."""

    access_key: str
    base_url: str = "https://api.hikerapi.com"
    timeout: float = 30.0
    cache_db_path: Path = Path("data/cache.sqlite")
    default_posts_sample: int = 12


def load_settings(env_file: Optional[str] = None) -> Settings:
    """
    Load settings from environment or an optional .env file.

    Raises:
        ValueError: if required keys are missing.
    """

    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    access_key = os.getenv("HIKER_ACCESS_KEY") or os.getenv("HIKERAPI_ACCESS_KEY")
    if not access_key:
        raise ValueError("HIKER_ACCESS_KEY is required. Add it to .env or your environment.")

    base_url = os.getenv("HIKER_BASE_URL", Settings.base_url)
    timeout = float(os.getenv("HIKER_TIMEOUT", Settings.timeout))
    cache_db_path = Path(os.getenv("CACHE_DB_PATH", Settings.cache_db_path))
    default_posts_sample = int(os.getenv("DEFAULT_POSTS_SAMPLE", Settings.default_posts_sample))

    cache_db_path.parent.mkdir(parents=True, exist_ok=True)

    return Settings(
        access_key=access_key,
        base_url=base_url,
        timeout=timeout,
        cache_db_path=cache_db_path,
        default_posts_sample=default_posts_sample,
    )

