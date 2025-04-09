"""
Settings module for the PyQt6 desktop application.
Provides a user interface for configuring application settings.
"""

import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QDialogButtonBox,
    QMessageBox,
    QTabWidget,
    QWidget,
)
from PyQt6.QtCore import QSize

from modules.config import config


class SettingsDialog(QDialog):
    """
    Settings dialog for configuring application settings.
    Allows users to modify configuration values through a UI.
    """

    def __init__(self, parent=None):
        """Initialize the settings dialog"""
        super().__init__(parent)
        self.setWindowTitle("アプリケーション設定")
        self.setMinimumSize(QSize(500, 300))

        self.setup_ui()
        self.load_current_settings()

    def setup_ui(self):
        """Set up the dialog UI"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Create AI Settings tab
        ai_tab = QWidget()
        ai_layout = QVBoxLayout()
        ai_tab.setLayout(ai_layout)

        # Form layout for inputs
        form_layout = QFormLayout()
        ai_layout.addLayout(form_layout)

        # OpenAI API Key field
        self.api_key_field = QLineEdit()
        self.api_key_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_field.setMinimumWidth(300)  # Set minimum width for API key field
        form_layout.addRow("OpenAI APIキー:", self.api_key_field)

        # AI Model text input
        self.model_input = QLineEdit()
        self.model_input.setMinimumWidth(300)  # Set minimum width for model input field
        form_layout.addRow("AIモデル:", self.model_input)

        # Add support note
        support_note = QLabel(
            "AIモデルは、gpt-4o, gpt-4o-mini, gpt-3.5-turbo "
            "等がサポートされています（OpenAIの公式ドキュメントを参照）。"
        )
        support_note.setWordWrap(True)
        ai_layout.addWidget(support_note)

        # Add tab to widget
        tab_widget.addTab(ai_tab, "AI設定")

        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_settings)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)

    def load_current_settings(self):
        """Load current settings from config into UI fields"""
        # Load API Key if available
        if config.OPEN_AI_API_KEY:
            self.api_key_field.setText(config.OPEN_AI_API_KEY)

        # Set current model in text input
        self.model_input.setText(config.AI_MODEL_NAME)

    def save_settings(self):
        """Save settings from UI to config"""
        try:
            # Get values from UI
            api_key = self.api_key_field.text().strip()
            model_name = self.model_input.text().strip()

            # Update environment variables
            if api_key:
                os.environ["OPEN_AI_API_KEY"] = api_key

            os.environ["AI_MODEL_NAME"] = model_name

            # Update config object
            config.OPEN_AI_API_KEY = api_key
            config.AI_MODEL_NAME = model_name

            # Write settings to .env file
            self.write_env_file()

            QMessageBox.information(self, "成功", "設定を保存しました！")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"設定の保存に失敗しました: {str(e)}")

    def write_env_file(self):
        """Write current settings to .env file"""
        env_path = config.APP_DIR / ".env"

        # Read existing content if file exists
        existing_lines = []
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                existing_lines = f.readlines()

        # Filter out the keys we're going to update
        filtered_lines = [
            line
            for line in existing_lines
            if not (
                line.startswith("OPEN_AI_API_KEY=") or line.startswith("AI_MODEL_NAME=")
            )
        ]

        # Add our settings
        if config.OPEN_AI_API_KEY:
            filtered_lines.append(f"OPEN_AI_API_KEY={config.OPEN_AI_API_KEY}\n")
        filtered_lines.append(f"AI_MODEL_NAME={config.AI_MODEL_NAME}\n")

        # Write back to file
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)
