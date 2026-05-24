# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QFrame, QVBoxLayout


class DomainWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("domainWindow")

        self.map_view = QWebEngineView()
        self.map_view.setObjectName("domainMap")
        self.map_view.setMinimumHeight(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(12)
        layout.addWidget(self.map_view, stretch=1)

        self.setStyleSheet(
            """
            QFrame#domainWindow {
                background: #f5f8fb;
            }

            QLabel#domainWindowTitle {
                color: #102a43;
                font-size: 24px;
                font-weight: 700;
            }

            QLabel#domainWindowText {
                color: #486581;
                font-size: 14px;
            }

            QWebEngineView#domainMap {
                border: 1px solid #d9e2ec;
                border-radius: 6px;
                background: #d9e8f5;
            }
            """
        )

        self.refresh()

    def refresh(self):
        self.map_view.load(QUrl.fromLocalFile(str(self.map_file_path())))

    def map_file_path(self):
        return Path(__file__).resolve().with_name("map.html")
