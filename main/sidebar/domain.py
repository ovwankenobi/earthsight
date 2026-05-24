# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

import json
from functools import partial

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QLineEdit,
    QMessageBox,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)

from domain_builder.domain_builder import domain_builder_settings
from main import project_settings

MODEL_TYPES = [
    "river_flooding",
    "surface_flooding",
    "coastal_flooding",
    "severe_wind",
    "rain_induced_landslide",
    "earthquake_induced_landslide",
    "debris_flow",
    "earthquake",
    "tsunami",
    "lahar_flow",
    "risk_assessment",
]


class Domain(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.domain_db_path = project_settings.domain_db_path

        self.setObjectName("domainSection")
        self.domain_buttons = {}
        self.selected_domain_json_path = None
        self.domain_selected_callback = None

        self.domain_label = QLabel("Domain")
        self.domain_label.setObjectName("sidebarSectionLabel")

        self.new_domain_button = QPushButton("+")
        self.new_domain_button.setObjectName("sidebarIconButton")
        self.new_domain_button.setFixedSize(28, 28)
        self.new_domain_button.clicked.connect(self.new_domain)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        header_layout.addWidget(self.domain_label)
        header_layout.addStretch()
        header_layout.addWidget(self.new_domain_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addLayout(header_layout)
        self.domain_list_layout = QVBoxLayout()
        self.domain_list_layout.setContentsMargins(0, 0, 0, 0)
        self.domain_list_layout.setSpacing(6)
        layout.addLayout(self.domain_list_layout)

        self.display_domains()

    def new_domain(self):
        self.domain_db_path = project_settings.domain_db_path
        if self.domain_db_path is None:
            QMessageBox.warning(self, "No Project Selected", "Please create or load a project first.")
            return

        dialog = NewDomainDialog(self)
        if dialog.exec() != QDialog.Accepted:
            return

        domain_name = dialog.domain_name()
        model_settings = dialog.model_settings()

        if not domain_name:
            QMessageBox.warning(self, "Missing Domain Name", "Please enter a domain name.")
            return

        if not any(model_settings.values()):
            QMessageBox.warning(self, "Missing Model Type", "Please select at least one model type.")
            return

        domain_path = self.domain_db_path / domain_name
        domain_json_path = domain_path / "domain.json"

        if domain_path.exists():
            QMessageBox.warning(
                self,
                "Domain Exists",
                f"The domain folder already exists:\n{domain_path}",
            )
            return

        try:
            domain_path.mkdir(parents=True)

            domain_config = {
                "domain": {
                    "name": domain_name,
                    "path": str(domain_path),
                },
                "folders": {
                    "domain_folder": str(domain_path),
                },
                "model_settings": model_settings,
            }

            with domain_json_path.open("w", encoding="utf-8") as config_file:
                json.dump(domain_config, config_file, indent=4)
        except OSError as error:
            QMessageBox.critical(
                self,
                "Domain Creation Failed",
                f"Could not create the domain:\n{error}",
            )
            return

        model_lines = [
            model_type
            for model_type, is_selected in model_settings.items()
            if is_selected
        ]

        QMessageBox.information(
            self,
            "Domain Created",
            f"Domain: {domain_name}\nFolder: {domain_path}\nModels:\n" + "\n".join(model_lines),
        )
        self.display_domains()
        self.select_domain(
            {
                "name": domain_name,
                "path": domain_path,
                "domain_json_path": domain_json_path,
                "config": domain_config,
            }
        )

    def list_domains(self):
        self.domain_db_path = project_settings.domain_db_path
        if self.domain_db_path is None or not self.domain_db_path.exists():
            return []

        domains = []
        for domain_path in self.domain_db_path.iterdir():
            if not domain_path.is_dir():
                continue

            domain_json_path = domain_path / "domain.json"
            if not domain_json_path.exists():
                continue

            try:
                with domain_json_path.open("r", encoding="utf-8") as config_file:
                    domain_config = json.load(config_file)
            except (OSError, json.JSONDecodeError):
                continue

            domain_name = domain_config.get("domain", {}).get("name")
            if not domain_name:
                continue

            domains.append(
                {
                    "name": domain_name,
                    "path": domain_path,
                    "domain_json_path": domain_json_path,
                    "config": domain_config,
                }
            )

        return domains

    def display_domains(self):
        self.clear_domain_buttons()
        domains = self.list_domains()

        for domain_info in domains:
            button = QPushButton(domain_info["name"])
            button.setObjectName("sidebarButton")
            button.setCheckable(True)
            button.clicked.connect(partial(self.select_domain, domain_info))

            self.domain_buttons[domain_info["domain_json_path"]] = button
            self.domain_list_layout.addWidget(button)

            if domain_info["domain_json_path"] == self.selected_domain_json_path:
                button.setChecked(True)

    def clear_domain_buttons(self):
        self.domain_buttons = {}

        while self.domain_list_layout.count():
            item = self.domain_list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def select_domain(self, domain_info, checked=False):
        self.selected_domain_json_path = domain_info["domain_json_path"]
        domain_builder_settings.register_domain(
            domain_info["config"],
            domain_info["domain_json_path"],
        )

        for domain_json_path, button in self.domain_buttons.items():
            button.setChecked(domain_json_path == self.selected_domain_json_path)

        if self.domain_selected_callback is not None:
            self.domain_selected_callback()


class NewDomainDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Domain")
        self.setMinimumWidth(380)

        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Domain name")

        self.model_checkboxes = []
        model_layout = QVBoxLayout()
        model_layout.setSpacing(6)

        for model_type in MODEL_TYPES:
            checkbox = QCheckBox(model_type)
            self.model_checkboxes.append(checkbox)
            model_layout.addWidget(checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)
        layout.addWidget(QLabel("Domain name"))
        layout.addWidget(self.domain_input)
        layout.addWidget(QLabel("What do you want to model?"))
        layout.addLayout(model_layout)
        layout.addWidget(buttons)

    def domain_name(self):
        return self.domain_input.text().strip()

    def model_settings(self):
        return {
            checkbox.text(): checkbox.isChecked()
            for checkbox in self.model_checkboxes
        }
