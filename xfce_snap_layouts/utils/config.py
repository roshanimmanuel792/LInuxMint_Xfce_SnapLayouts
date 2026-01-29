"""Configuration management for xfce-snap-layouts."""

import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "keyboard_shortcut": "<Super>z",
    "enabled_layouts": [
        "50_50_split",
        "1_big_2_small",
        "3_columns"
    ],
    "layout_ratios": {
        "50_50_split": {
            "left": {"x": 0, "y": 0, "width": 0.5, "height": 1.0},
            "right": {"x": 0.5, "y": 0, "width": 0.5, "height": 1.0}
        },
        "1_big_2_small": {
            "big": {"x": 0, "y": 0, "width": 0.6, "height": 1.0},
            "small_top": {"x": 0.6, "y": 0, "width": 0.4, "height": 0.5},
            "small_bottom": {"x": 0.6, "y": 0.5, "width": 0.4, "height": 0.5}
        },
        "3_columns": {
            "left": {"x": 0, "y": 0, "width": 0.333, "height": 1.0},
            "center": {"x": 0.333, "y": 0, "width": 0.334, "height": 1.0},
            "right": {"x": 0.667, "y": 0, "width": 0.333, "height": 1.0}
        }
    },
    "overlay_opacity": 0.9,
    "zone_highlight_color": "#0078d4",
    "zone_highlight_opacity": 0.3
}


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "xfce-snap-layouts"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        try:
            if self.config_file.exists():
                logger.info(f"Loading config from {self.config_file}")
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all required keys exist
                    return {**DEFAULT_CONFIG, **loaded}
            else:
                logger.info("No config file found, using defaults")
                self._save_default_config()
                return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading config: {e}, using defaults")
            return DEFAULT_CONFIG.copy()
    
    def _save_default_config(self) -> None:
        """Save default configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
            logger.info(f"Default config saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self.config = self._load_config()
        logger.info("Configuration reloaded")


# Global config instance
config_manager = ConfigManager()
