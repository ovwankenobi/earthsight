# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

import json
from pathlib import Path

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMenu, QMessageBox, QPushButton

from main import project_settings


class Project(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Project", parent)
        self.project_name = None
        self.project_changed_callback = None
        self.setObjectName("sidebarButton")
        self.clicked.connect(self.show_project_menu)

    def show_project_menu(self):
        menu = QMenu(self)
        menu.setObjectName("projectMenu")

        new_project_action = menu.addAction("New Project")
        load_project_action = menu.addAction("Load Project")

        new_project_action.triggered.connect(lambda: self.new_proj())
        load_project_action.triggered.connect(lambda: self.load_proj())

        menu.setStyleSheet(
            """
            QMenu#projectMenu {
                background: #ffffff;
                border: 1px solid #d9e2ec;
                border-radius: 6px;
                padding: 6px;
            }

            QMenu#projectMenu::item {
                color: #243b53;
                padding: 8px 32px 8px 12px;
                border-radius: 4px;
            }

            QMenu#projectMenu::item:selected {
                background: #eef4fb;
            }
            """
        )

        menu_position = self.mapToGlobal(QPoint(self.width() + 4, 0))
        menu.exec(menu_position)

    def new_proj(self):
        project_name, accepted = QInputDialog.getText(
            self,
            "New Project",
            "Project name:",
        )

        project_name = project_name.strip()
        if not accepted or not project_name:
            return

        parent_folder = QFileDialog.getExistingDirectory(
            self,
            "Choose where to create the project folder",
        )
        if not parent_folder:
            return

        project_path = Path(parent_folder) / project_name
        if project_path.exists():
            QMessageBox.warning(
                self,
                "Project Exists",
                f"The folder already exists:\n{project_path}",
            )
            return

        domain_db_path = project_path / "domain_db"
        meteo_db_path = project_path / "meteo_db"
        run_folder_path = project_path / "run_folder"

        try:
            domain_db_path.mkdir(parents=True)
            meteo_db_path.mkdir()
            run_folder_path.mkdir()

            project_config = {
                "project": {
                    "name": project_name,
                    "path": str(project_path),
                },
                "folders": {
                    "domain_db": str(domain_db_path),
                    "meteo_db": str(meteo_db_path),
                    "run_folder": str(run_folder_path),
                },
            }

            project_json_path = project_path / "project.json"
            with project_json_path.open("w", encoding="utf-8") as config_file:
                json.dump(project_config, config_file, indent=4)
        except OSError as error:
            QMessageBox.critical(
                self,
                "Project Creation Failed",
                f"Could not create the project:\n{error}",
            )
            return

        QMessageBox.information(
            self,
            "Project Created",
            f"Created project folder:\n{project_path}",
        )
        project_settings.register_project(project_config, project_json_path)
        self.set_project_name(project_name)
        self.notify_project_changed()

    def load_proj(self):
        project_folder = QFileDialog.getExistingDirectory(
            self,
            "Choose project folder",
        )
        if not project_folder:
            return

        project_path = Path(project_folder)
        project_json = project_path / "project.json"

        if not project_json.exists():
            QMessageBox.critical(
                self,
                "Invalid Project Folder",
                "project.json could not be found in the selected folder.",
            )
            return

        try:
            with project_json.open("r", encoding="utf-8") as config_file:
                project_config = json.load(config_file)
        except (OSError, json.JSONDecodeError) as error:
            QMessageBox.critical(
                self,
                "Project Load Failed",
                f"Could not read project.json:\n{error}",
            )
            return

        project_name = project_config.get("project", {}).get("name", project_path.name)

        QMessageBox.information(
            self,
            "Project Loaded",
            f"Loaded project:\n{project_path}",
        )
        project_settings.register_project(project_config, project_json)
        self.set_project_name(project_name)
        self.notify_project_changed()

    def set_project_name(self, project_name):
        self.project_name = project_name
        self.setText(f"Project ({project_name})")

    def notify_project_changed(self):
        if self.project_changed_callback is not None:
            self.project_changed_callback()
