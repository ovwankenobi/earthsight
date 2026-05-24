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
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from domain_builder.domain_window import DomainWindow
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
        self.sidebar.domain.domain_selected_callback = self.show_domain_window

        self.status_label = QLabel("Select Project or Domain from the sidebar.")
        self.status_label.setObjectName("statusLabel")
        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.status_label)

        self.header.sidebar_toggled.connect(self.toggle_sidebar)

        content = QWidget()
        content.setObjectName("mainContent")

        body = QWidget()
        body.setObjectName("mainBody")

        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content_stack, stretch=1)

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

    def show_domain_window(self):
        domain_window = DomainWindow()
        self.content_stack.addWidget(domain_window)
        self.content_stack.setCurrentWidget(domain_window)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
