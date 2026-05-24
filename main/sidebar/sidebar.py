# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout

from sidebar.domain import Domain
from sidebar.project import Project


class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("appSidebar")
        self.setFixedWidth(220)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.domain = Domain()
        self.project_button = Project()
        self.project_button.project_changed_callback = self.domain.display_domains

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(10)
        layout.addWidget(self.project_button)
        layout.addSpacing(12)
        layout.addWidget(self.domain)
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

            QPushButton#sidebarButton:checked {
                background: #d9e8f5;
                border-color: #7fb3d5;
                color: #102a43;
            }

            QPushButton#sidebarIconButton {
                background: transparent;
                color: #243b53;
                border: 1px solid transparent;
                border-radius: 6px;
                font-size: 18px;
                font-weight: 700;
            }

            QPushButton#sidebarIconButton:hover {
                background: #eef4fb;
                border-color: #bcccdc;
            }

            QPushButton#sidebarIconButton:pressed {
                background: #d9e8f5;
            }

            QLabel#sidebarSectionLabel {
                color: #627d98;
                font-size: 14px;
                font-weight: 700;
                padding: 8px 12px 0 12px;
            }
            """
        )
