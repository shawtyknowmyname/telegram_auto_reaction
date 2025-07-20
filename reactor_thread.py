# file: reactor_thread.py
import asyncio
from pathlib import Path
from PyQt5.QtCore import QThread
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from config_manager import ConfigManager


class ReactorThread(QThread):
    def __init__(self, config: ConfigManager):
        super().__init__()
        self.cfg = config
        self._reactor_event = asyncio.Event()
        self.app = None

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main())

    def stop(self):
        if self.app:
            try:
                self._reactor_event.set()
            except Exception:
                pass

    async def main(self):
        try:
            print(f"➡️ Проверка запуска сессии: {self.cfg.session_name}")
            session_path = str(Path("sessions") / self.cfg.session_name)

            self.app = Client(
                session_path,
                api_id=self.cfg.api_id,
                api_hash=self.cfg.api_hash
            )

            async with self.app as app:
                print(f"✅ Сессия успешно запущена: {self.cfg.session_name}")
                print(f"➡️ Реакция по умолчанию: {self.cfg.default_reaction}")
                print(f"➡️ Кастомные реакции: {self.cfg.custom_reactions}")
                print(f"➡️ Разрешены в ЛС: {'все' if self.cfg.react_pm_mode == 'all' else self.cfg.allowed_pm_users}")
                print(f"➡️ Разрешены в группах: {'все' if self.cfg.react_group_mode == 'all' else self.cfg.allowed_group_users}")
                print(f"➡️ Реагировать на себя в ЛС: {self.cfg.react_to_self_in_pm}")
                print(f"➡️ Реагировать на себя в группах: {self.cfg.react_to_self_in_groups}")

                allowed_pm_users = [u.lower() for u in self.cfg.allowed_pm_users]
                allowed_group_users = [u.lower() for u in self.cfg.allowed_group_users]

                @app.on_message(filters.group | filters.private)
                async def handle_message(client: Client, message: Message):
                    sender = message.from_user
                    if not sender:
                        return

                    username = (sender.username or "").lower()
                    chat_type = getattr(message.chat, "type", None)
                    is_private = chat_type == ChatType.PRIVATE

                    if sender.is_self:
                        if is_private and not self.cfg.react_to_self_in_pm:
                            print("[DEBUG] Пропущено своё сообщение в ЛС")
                            return
                        if not is_private and not self.cfg.react_to_self_in_groups:
                            print("[DEBUG] Пропущено своё сообщение в группе")
                            return

                    allowed_pm = self.cfg.react_pm_mode == "all" or username in allowed_pm_users
                    allowed_group = self.cfg.react_group_mode == "all" or username in allowed_group_users

                    if (is_private and allowed_pm) or (not is_private and allowed_group):
                        reaction = self.cfg.custom_reactions.get(username) or self.cfg.default_reaction
                        try:
                            chat_title = message.chat.title if not is_private else "PM"
                            print(f"[{chat_title}] -> {username}: {reaction}")
                            await message.react(reaction)
                        except Exception as e:
                            print(f"❌ Ошибка при реакции: {e}")

                print("🤡 Auto Reaction запущен!")
                await self._reactor_event.wait()

        except Exception as e:
            print(f"❌ Ошибка запуска клиента: {e}")
