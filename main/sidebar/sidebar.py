# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

from configparser import ConfigParser
from pathlib import Path

from PySide6.QtCore import QPoint, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QInputDialog,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class Sidebar(QFrame):
    project_clicked = Signal()
    model_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("appSidebar")
        self.setFixedWidth(220)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.project_button = Project()
        self.project_button.project_clicked.connect(lambda: self.project_clicked.emit())

        self.model_button = QPushButton("Model")
        self.model_button.setObjectName("sidebarButton")
        self.model_button.clicked.connect(lambda: self.model_clicked.emit())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(10)
        layout.addWidget(self.project_button)
        layout.addWidget(self.model_button)
        layout.addStretch()

        self.setStyleSheet(
            """
            QFrame#appSidebar {
                background: #ffffff;
                border-right: 1px solid #d9e2ec;
            }

            QPushButton#sidebarButton {
                background: transparent;
                color: #243b53;
                border: 1px solid transparent;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                padding: 10px 12px;
                text-align: left;
            }

            QPushButton#sidebarButton:hover {
                background: #eef4fb;
                border-color: #bcccdc;
            }

            QPushButton#sidebarButton:pressed {
                background: #d9e8f5;
            }
            """
        )
        
class Project(QPushButton):
    project_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__("Project", parent)
        self.project_name = None
        self.setObjectName("sidebarButton")
        self.clicked.connect(self.show_project_menu)

    def show_project_menu(self):
        self.project_clicked.emit()

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

            config = ConfigParser()
            config["project"] = {
                "name": project_name,
                "path": str(project_path),
            }
            config["folders"] = {
                "domain_db": str(domain_db_path),
                "meteo_db": str(meteo_db_path),
                "run_folder": str(run_folder_path),
            }

            with (project_path / "project.ini").open("w", encoding="utf-8") as config_file:
                config.write(config_file)
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
        self.set_project_name(project_name)

    def load_proj(self):
        project_folder = QFileDialog.getExistingDirectory(
            self,
            "Choose project folder",
        )
        if not project_folder:
            return

        project_path = Path(project_folder)
        project_ini = project_path / "project.ini"

        if not project_ini.exists():
            QMessageBox.critical(
                self,
                "Invalid Project Folder",
                "project.ini could not be found in the selected folder.",
            )
            return

        config = ConfigParser()
        config.read(project_ini, encoding="utf-8")
        project_name = config.get("project", "name", fallback=project_path.name)

        QMessageBox.information(
            self,
            "Project Loaded",
            f"Loaded project:\n{project_path}",
        )
        self.set_project_name(project_name)

    def set_project_name(self, project_name):
        self.project_name = project_name
        self.setText(f"Project ({project_name})")
