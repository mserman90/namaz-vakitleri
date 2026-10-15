"""
Kullanıcı Ayarları ve Tercihleri Yönetimi.
"""

import os
import json
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "selected_province": "34 - İstanbul",
    "theme_mode": "dark",  # 'dark', 'light', 'system'
    "sound_enabled": True,
    "notify_on_prayer": True,
    "notify_minutes_before": 15,  # 0: kapalı, 15: 15 dk önce
    "minimize_to_tray": True
}


class ConfigManager:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(config_dir, "config.json")
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cfg = DEFAULT_CONFIG.copy()
                    cfg.update(data)
                    return cfg
            except Exception:
                pass
        return DEFAULT_CONFIG.copy()

    def save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save()
