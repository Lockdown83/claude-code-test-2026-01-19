"""Configuration management for VC Dashboard CLI."""
import json
from pathlib import Path
from typing import Dict, Any


CONFIG_DIR = Path.home() / ".vc-dashboard"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "api_url": "http://localhost:8000",
    "default_limit": 20,
    "output_format": "table",  # table, json, compact
    "show_colors": True
}


def load_config() -> Dict[str, Any]:
    """Load configuration from file or return defaults.

    Returns:
        Dictionary containing configuration settings.
    """
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                user_config = json.load(f)
                return {**DEFAULT_CONFIG, **user_config}
        except (json.JSONDecodeError, IOError):
            # If config file is corrupted, return defaults
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file.

    Args:
        config: Dictionary containing configuration settings to save.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_api_url() -> str:
    """Get API URL from configuration.

    Returns:
        API base URL string.
    """
    return load_config()['api_url']


def set_api_url(url: str) -> None:
    """Set API URL in configuration.

    Args:
        url: New API base URL.
    """
    config = load_config()
    config['api_url'] = url.rstrip('/')
    save_config(config)
