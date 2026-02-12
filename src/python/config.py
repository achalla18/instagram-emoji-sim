"""
Configuration loader for Emoji Reactions desktop app.
Reads settings.json and provides typed access.
"""

import json
import os
from pathlib import Path


def load_config() -> dict:
    """Load config from settings.json, searching up from this file."""
    config_paths = [
        Path(__file__).parent.parent.parent / "config" / "settings.json",
        Path.cwd() / "config" / "settings.json",
        Path.cwd() / "settings.json",
    ]
    for path in config_paths:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    
    # Fallback defaults
    return {
        "window": {"width": 420, "height": 700, "background": "#1a1a2e",
                    "always_on_top": True, "transparency": 0.95},
        "emojis": [
            {"icon": "❤️", "label": "Love", "color": "#ff3b5c"},
            {"icon": "😂", "label": "Haha", "color": "#ffcc00"},
            {"icon": "😮", "label": "Wow", "color": "#ff9500"},
            {"icon": "😢", "label": "Sad", "color": "#5ac8fa"},
            {"icon": "😡", "label": "Angry", "color": "#ff2d55"},
            {"icon": "👍", "label": "Like", "color": "#34c759"},
        ],
        "animation": {
            "rise_speed_min": 1.5, "rise_speed_max": 3.5,
            "wobble_amplitude": 30, "wobble_frequency": 0.03,
            "initial_scale": 0.3, "max_scale": 1.2,
            "fade_start": 0.7, "lifetime_ms": 3000,
            "spawn_size": 42, "max_active": 50,
        },
        "particles": {
            "enabled": True, "count_per_emoji": 6,
            "trail_length": 8, "size_min": 2, "size_max": 6,
            "spread": 15, "opacity": 0.6,
        },
    }


# Module-level config instance
CONFIG = load_config()
