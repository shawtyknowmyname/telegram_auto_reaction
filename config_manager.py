# file: config_manager.py
import json
import os
from pathlib import Path
from typing import List, Dict, Union


class ConfigManager:
    def __init__(self, config_path=None, reactions_path=None):
        session_dir = Path("sessions")
        session_dir.mkdir(exist_ok=True)

        self.config_path = config_path or session_dir / "config.json"
        self.reactions_path = reactions_path or session_dir / "reactions.json"

        self.api_id: Union[int, None] = None
        self.api_hash: Union[str, None] = None
        self.session_name: str = "clown"

        self.react_pm_mode: str = "all"  # 'all' or 'specific'
        self.allowed_pm_users: List[Union[int, str]] = []

        self.react_group_mode: str = "all" # 'all' or 'specific'
        self.allowed_group_users: List[Union[int, str]] = []

        self.react_to_self_in_groups: bool = False

        self.default_reaction: str = "🤡"
        self.custom_reactions: Dict[Union[str, int], str] = {}

    def input_config(self):
        print("\n=== Настройка авторизации ===")
        self.api_id = int(input("API ID: ").strip())
        self.api_hash = input("API HASH: ").strip()
        self.session_name = input("Session name: ").strip() or "clown"

        print("\n=== Настройки личных сообщений ===")
        self.react_pm_mode = "all" if input("[1] Все / [2] Только определенные: ").strip() == "1" else "specific"
        if self.react_pm_mode == "specific":
            self.allowed_pm_users = [s.strip() for s in input("Usernames через запятую: ").split(",")]

        print("\n=== Настройки групп ===")
        self.react_group_mode = "all" if input("[1] Все / [2] Только определенные: ").strip() == "1" else "specific"
        if self.react_group_mode == "specific":
            self.allowed_group_users = [s.strip() for s in input("Usernames через запятую: ").split(",")]

        self.react_to_self_in_groups = input("Реагировать на свои сообщения в группах? (y/N): ").strip().lower() == "y"

        print("\n=== Настройки реакций ===")
        self.default_reaction = input("Реакция по умолчанию (например 🤡): ").strip() or "🤡"
        raw = input("Кастомные реакции (username:emoji): ").strip()
        for pair in raw.split(","):
            if ":" in pair:
                key, value = pair.strip().split(":")
                self.custom_reactions[key.strip()] = value.strip()

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump({
                "api_id": self.api_id,
                "api_hash": self.api_hash,
                "session_name": self.session_name,
                "react_pm_mode": self.react_pm_mode,
                "allowed_pm_users": self.allowed_pm_users,
                "react_group_mode": self.react_group_mode,
                "allowed_group_users": self.allowed_group_users,
                "default_reaction": self.default_reaction,
                "react_to_self_in_groups": self.react_to_self_in_groups
            }, f, indent=4, ensure_ascii=False)

        with open(self.reactions_path, "w", encoding="utf-8") as f:
            json.dump(self.custom_reactions, f, indent=4, ensure_ascii=False)

    def load(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.api_id = data["api_id"]
        self.api_hash = data["api_hash"]
        self.session_name = data.get("session_name", "clown_reactor")
        self.react_pm_mode = data.get("react_pm_mode", "all")
        self.allowed_pm_users = data.get("allowed_pm_users", [])
        self.react_group_mode = data.get("react_group_mode", "all")
        self.allowed_group_users = data.get("allowed_group_users", [])
        self.default_reaction = data.get("default_reaction", "🤡")
        self.react_to_self_in_groups = data.get("react_to_self_in_groups", False)

        with open(self.reactions_path, "r", encoding="utf-8") as f:
            self.custom_reactions = json.load(f)

if __name__ == "__main__":
    cfg = ConfigManager()
    cfg.input_config()
    cfg.save()
    print("\n✅ Конфигурация успешно сохранена в sessions/config.json и reactions.json")
