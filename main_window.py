# file: main_window.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QRadioButton, QLineEdit, QTextEdit,
    QPushButton, QMessageBox, QComboBox, QButtonGroup, QCheckBox
)
from config_manager import ConfigManager
from reactor_thread import ReactorThread
import os


class MainWindow(QWidget):
    def __init__(self, config_data):
        super().__init__()
        self.setWindowTitle("Clown Reactor - Настройки")
        self.setFixedSize(600, 530)

        session_name = os.path.basename(config_data["session_name"])
        self.cfg = ConfigManager()
        self.cfg.session_name = session_name

        if self.cfg.config_path.exists():
            self.cfg.load()
        else:
            self.cfg.api_id = config_data["api_id"]
            self.cfg.api_hash = config_data["api_hash"]
            self.cfg.session_name = session_name

        self.init_ui()
        self.load_into_ui()
        self.reactor_thread = None

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Настройки ЛС:"))
        self.pm_all = QRadioButton("Реагировать в ЛС на всех")
        self.pm_spec = QRadioButton("Только на определённых")
        self.pm_group = QButtonGroup()
        self.pm_group.addButton(self.pm_all)
        self.pm_group.addButton(self.pm_spec)

        self.pm_users = QLineEdit()
        self.pm_users.setPlaceholderText("username, username2")

        self.react_self_pm_checkbox = QCheckBox("Ставить реакции на свои сообщения в ЛС")

        layout.addWidget(self.pm_all)
        layout.addWidget(self.pm_spec)
        layout.addWidget(self.pm_users)
        layout.addWidget(self.react_self_pm_checkbox)

        layout.addWidget(QLabel("Настройки групп:"))
        self.grp_all = QRadioButton("Реагировать в группах на всех")
        self.grp_spec = QRadioButton("Только на определённых")
        self.grp_group = QButtonGroup()
        self.grp_group.addButton(self.grp_all)
        self.grp_group.addButton(self.grp_spec)

        self.grp_users = QLineEdit()
        self.grp_users.setPlaceholderText("username, username2")

        self.react_self_checkbox = QCheckBox("Ставить реакции на свои сообщения в группах")

        layout.addWidget(self.grp_all)
        layout.addWidget(self.grp_spec)
        layout.addWidget(self.grp_users)
        layout.addWidget(self.react_self_checkbox)

        layout.addWidget(QLabel("Реакция по умолчанию:"))
        self.reaction_combo = QComboBox()
        self.reaction_combo.addItems(["🤡", "💩", "🔥", "😎", "❤️", "👀", "🤔"])
        self.custom_reaction = QLineEdit()
        self.custom_reaction.setPlaceholderText("Своё эмодзи...")

        layout.addWidget(self.reaction_combo)
        layout.addWidget(self.custom_reaction)

        layout.addWidget(QLabel("Кастомные реакции (username:emoji):"))
        self.customs = QTextEdit()
        self.customs.setPlaceholderText("username:🤡\nusername2:🔥")
        layout.addWidget(self.customs)

        self.save_button = QPushButton("💾 Сохранить настройки")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        self.run_button = QPushButton("▶️ Запустить Auto Reaction")
        self.run_button.clicked.connect(self.run)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def load_into_ui(self):
        if self.cfg.react_pm_mode == "all":
            self.pm_all.setChecked(True)
        else:
            self.pm_spec.setChecked(True)
            self.pm_users.setText(", ".join(self.cfg.allowed_pm_users))

        if self.cfg.react_group_mode == "all":
            self.grp_all.setChecked(True)
        else:
            self.grp_spec.setChecked(True)
            self.grp_users.setText(", ".join(self.cfg.allowed_group_users))

        self.react_self_pm_checkbox.setChecked(self.cfg.react_to_self_in_pm)
        self.react_self_checkbox.setChecked(self.cfg.react_to_self_in_groups)

        self.reaction_combo.setCurrentText(self.cfg.default_reaction)
        self.custom_reaction.setText("")

        lines = "\n".join(f"{k}:{v}" for k, v in self.cfg.custom_reactions.items())
        self.customs.setPlainText(lines)

    def save(self):
        self.cfg.react_pm_mode = "all" if self.pm_all.isChecked() else "specific"
        self.cfg.allowed_pm_users = [u.strip() for u in self.pm_users.text().split(",") if u.strip()]

        self.cfg.react_group_mode = "all" if self.grp_all.isChecked() else "specific"
        self.cfg.allowed_group_users = [u.strip() for u in self.grp_users.text().split(",") if u.strip()]

        self.cfg.react_to_self_in_pm = self.react_self_pm_checkbox.isChecked()
        self.cfg.react_to_self_in_groups = self.react_self_checkbox.isChecked()

        selected = self.reaction_combo.currentText()
        custom = self.custom_reaction.text().strip()
        self.cfg.default_reaction = custom if custom else selected

        self.cfg.custom_reactions.clear()
        for line in self.customs.toPlainText().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                self.cfg.custom_reactions[k.strip()] = v.strip()

        self.cfg.session_name = os.path.basename(self.cfg.session_name)
        self.cfg.save()
        QMessageBox.information(self, "Сохранено", "Настройки успешно сохранены.")

    def stop_old_reactor(self):
        if self.reactor_thread and self.reactor_thread.isRunning():
            self.reactor_thread.stop()
            self.reactor_thread.quit()
            self.reactor_thread.wait()

    def run(self):
        self.save()
        self.stop_old_reactor()
        self.reactor_thread = ReactorThread(self.cfg)
        self.reactor_thread.start()
        QMessageBox.information(self, "Auto Reaction", "Auto Reaction запущен в фоновом режиме.")
