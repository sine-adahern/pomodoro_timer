"""
storage.py - Persistent settings and total study time storage using JSON
"""
import json
from pathlib import Path
from typing import Dict, Any


class Storage:
    """Handle loading and saving settings to a JSON file."""
    
    def __init__(self):
        # Create settings directory in user's home
        self.settings_dir = Path.home() / ".pomo_timer"
        self.settings_dir.mkdir(exist_ok=True)
        self.settings_file = self.settings_dir / "settings.json"
        
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from JSON file, or return defaults if file doesn't exist."""
        defaults = {
            "study_minutes": 30,
            "break_minutes": 5,
            "total_study_seconds": 0,
            "theme": {
                "background_color": "#FFE5EC",  # Soft pink
                "card_color": "#FFD6E0",        # Light pink
                "accent_color": "#FF9BB5",      # Darker pink
                "progress_color": "#FF9BB5",    # Progress fill color
                "text_color": "#FFFFFF"         # White for timer text
            }
        }
        
        if not self.settings_file.exists():
            return defaults
        
        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
                # Merge with defaults to handle missing keys
                for key, value in defaults.items():
                    if key not in data:
                        data[key] = value
                # Ensure theme dict has all keys
                if "theme" in data:
                    for theme_key, theme_value in defaults["theme"].items():
                        if theme_key not in data["theme"]:
                            data["theme"][theme_key] = theme_value
                return data
        except (json.JSONDecodeError, IOError):
            return defaults
    
    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Save settings to JSON file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def update_total_study_seconds(self, total_seconds: float) -> None:
        """Update only the total study seconds in the settings file."""
        settings = self.load_settings()
        settings["total_study_seconds"] = total_seconds
        self.save_settings(settings)
    
    def reset_total_study_seconds(self) -> None:
        """Reset total study time to zero."""
        settings = self.load_settings()
        settings["total_study_seconds"] = 0
        self.save_settings(settings)
