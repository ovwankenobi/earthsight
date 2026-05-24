# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy


class Header(QFrame):
    sidebar_toggled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("appHeader")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.sidebar_button = QPushButton("☰")
        self.sidebar_button.setObjectName("sidebar_button")
        self.sidebar_button.setFixedSize(40, 40)
        self.sidebar_button.clicked.connect(lambda: self.sidebar_toggled.emit())

        title = QLabel("Earth Sight")
        title.setObjectName("appTitle")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 20, 10)
        layout.setSpacing(12)
        layout.addWidget(self.sidebar_button)
        layout.addWidget(title)
        layout.addStretch()

        self.setStyleSheet(
            """
            QFrame#appHeader {
                background: #ffffff;
                border-bottom: 1px solid #d9e2ec;
            }

            QLabel#appTitle {
                color: #102a43;
                font-size: 18px;
                font-weight: 700;
            }

            QPushButton#sidebar_button {
                background: #eef4fb;
                color: #243b53;
                border: 1px solid #d9e2ec;
                border-radius: 6px;
                font-size: 18px;
                font-weight: 700;
            }

            QPushButton#sidebar_button:hover {
                background: #d9e8f5;
            }

            QPushButton#sidebar_button:pressed {
                background: #c8dff0;
            }
            """
        )
