# file: auth_window.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
from pyrogram import Client
import os


class AuthWindow(QWidget):
    auth_success = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация Telegram")
        self.setFixedSize(400, 300)
        self.phone = ""
        self.app = None

        self.api_id_input = QLineEdit()
        self.api_hash_input = QLineEdit()
        self.session_input = QLineEdit("clown")
        self.phone_input = QLineEdit()
        self.code_input = QLineEdit()

        self.stage = 0
        self.init_ui()

        os.makedirs("sessions", exist_ok=True)

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("API ID:"))
        layout.addWidget(self.api_id_input)
        layout.addWidget(QLabel("API HASH:"))
        layout.addWidget(self.api_hash_input)
        layout.addWidget(QLabel("Session name:"))
        layout.addWidget(self.session_input)

        self.phone_input.setPlaceholderText("+123456789")
        self.code_input.setPlaceholderText("Код из Telegram")
        layout.addWidget(QLabel("Номер телефона:"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Код подтверждения:"))
        layout.addWidget(self.code_input)

        self.code_input.setEnabled(False)

        self.auth_button = QPushButton("🔐 Авторизоваться")
        self.auth_button.clicked.connect(self.handle_auth)
        layout.addWidget(self.auth_button)

        self.setLayout(layout)

    def handle_auth(self):
        try:
            api_id = int(self.api_id_input.text().strip())
            api_hash = self.api_hash_input.text().strip()
            session_name = self.session_input.text().strip()
            session_path = os.path.join("sessions", session_name)

            if self.stage == 0:
                self.phone = self.phone_input.text().strip()
                self.app = Client(session_path, api_id=api_id, api_hash=api_hash)
                self.app.connect()
                self.sent_code = self.app.send_code(self.phone)
                self.phone_code_hash = self.sent_code.phone_code_hash
                self.code_input.setEnabled(True)
                self.stage = 1
                QMessageBox.information(self, "Код отправлен", "Код отправлен в Telegram")

            elif self.stage == 1:
                code = self.code_input.text().strip()
                self.app.sign_in(phone_number=self.phone, phone_code=code, phone_code_hash=self.phone_code_hash)
                self.app.disconnect()
                QMessageBox.information(self, "Успех", "Вы успешно авторизовались!")

                self.auth_success.emit({
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_name": session_name
                })

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
