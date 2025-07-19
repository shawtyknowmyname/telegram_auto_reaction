# file: gui_app.py
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QStackedWidget
from auth_window import AuthWindow
from main_window import MainWindow
from config_manager import ConfigManager


class ClownApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Auto Reaction 🤡")
        self.setFixedSize(620, 540)

        self.cfg = ConfigManager()

        try:
            self.cfg.load()
            session_path = Path("sessions") / self.cfg.session_name
            if not (session_path.with_suffix(".session")).exists():
                raise FileNotFoundError
            self.load_main_screen({
                "api_id": self.cfg.api_id,
                "api_hash": self.cfg.api_hash,
                "session_name": str(session_path)
            })
        except FileNotFoundError:
            self.auth_screen = AuthWindow()
            self.auth_screen.auth_success.connect(self.load_main_screen)
            self.addWidget(self.auth_screen)
            self.setCurrentWidget(self.auth_screen)

    def load_main_screen(self, config_data):
        try:
            self.main_screen = MainWindow(config_data)
            self.addWidget(self.main_screen)
            self.setCurrentWidget(self.main_screen)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("❌ Ошибка при загрузке основного окна:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClownApp()
    window.show()
    sys.exit(app.exec_())