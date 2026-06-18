import json
import os
from pathlib import Path


class ConfigManager:
    """管理配置文件（API Key、历史记录、输出目录等）"""

    def __init__(self, app_dir: str | None = None):
        if app_dir is None:
            app_dir = Path(__file__).resolve().parent
        self.app_dir = Path(app_dir)
        self.config_file = self.app_dir / "config.json"
        self.history_file = self.app_dir / "history.json"
        self._default_config = {
            "ai": {
                "base_url": "",
                "api_key": "",
                "model": "deepseek-chat",
                "temperature": 0.7,
            },
            "output": {
                "output_dir": str(self.app_dir / "output"),
                "save_to_same_dir": False,
            },
            "ui": {
                "theme": "green-light",
                "last_tab": 0,
            },
        }
        self.config = self._load_config()
        self.history = self._load_history()

    def _load_config(self) -> dict:
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = self._deep_merge(self._default_config, data)
                return merged
            except Exception:
                pass
        return json.loads(json.dumps(self._default_config))

    def _load_history(self) -> list:
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _deep_merge(self, base: dict, override: dict) -> dict:
        result = dict(base)
        for k, v in override.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = self._deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    def save_config(self) -> None:
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def save_history(self) -> None:
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # AI 配置
    def get_ai_config(self) -> dict:
        return dict(self.config.get("ai", {}))

    def set_ai_config(self, **kwargs) -> None:
        if "ai" not in self.config:
            self.config["ai"] = {}
        for k, v in kwargs.items():
            self.config["ai"][k] = v
        self.save_config()

    # 输出配置
    def get_output_config(self) -> dict:
        return dict(self.config.get("output", {}))

    def set_output_config(self, **kwargs) -> None:
        if "output" not in self.config:
            self.config["output"] = {}
        for k, v in kwargs.items():
            self.config["output"][k] = v
        self.save_config()

    # 历史记录
    def add_history(self, item: dict) -> None:
        self.history.insert(0, item)
        if len(self.history) > 50:
            self.history = self.history[:50]
        self.save_history()

    def get_history(self) -> list:
        return list(self.history)

    def clear_history(self) -> None:
        self.history = []
        self.save_history()

    # UI 状态
    def get_last_tab(self) -> int:
        return int(self.config.get("ui", {}).get("last_tab", 0))

    def set_last_tab(self, index: int) -> None:
        if "ui" not in self.config:
            self.config["ui"] = {}
        self.config["ui"]["last_tab"] = int(index)
        self.save_config()
