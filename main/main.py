# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from header import Header
from sidebar.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EarthSight")
        self.resize(1100, 720)

        self.header = Header()
        self.sidebar = Sidebar()
        self.sidebar.hide()
        self.status_label = QLabel("Select Project or Model from the sidebar.")
        self.status_label.setObjectName("statusLabel")

        self.header.sidebar_toggled.connect(self.toggle_sidebar)
        self.sidebar.project_clicked.connect(self.show_project)
        self.sidebar.model_clicked.connect(self.show_model)

        content = QWidget()
        content.setObjectName("mainContent")

        body = QWidget()
        body.setObjectName("mainBody")

        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.status_label, stretch=1)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.header)
        layout.addWidget(body, stretch=1)

        self.setCentralWidget(content)
        self.setStyleSheet(
            """
            QWidget#mainContent {
                background: #f5f8fb;
            }

            QWidget#mainBody {
                background: #f5f8fb;
            }

            QLabel#statusLabel {
                color: #486581;
                font-size: 18px;
                padding: 28px;
            }
            """
        )

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def show_project(self):
        self.status_label.setText("Project selected")

    def show_model(self):
        self.status_label.setText("Model selected")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
