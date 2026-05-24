# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

from pathlib import Path


class ProjectSettings:
    def __init__(self):
        self.clear()

    def clear_orig(self):
        self.project_name = None
        self.project_path = None
        self.project_json_path = None
        self.domain_db_path = None
        self.meteo_db_path = None
        self.run_folder_path = None

    def clear(self):
        self.project_name = "Sample"
        self.project_path = "D:\projects\Flood_Model\Sample"
        self.project_json_path = Path(self.project_path) / "project.json"
        self.domain_db_path = Path(self.project_path) / "domain_db"
        self.meteo_db_path = Path(self.project_path) / "meteo_db"
        self.run_folder_path = Path(self.project_path) / "run_folder"

    def register_project(self, project_config, project_json_path):
        project = project_config.get("project", {})
        folders = project_config.get("folders", {})

        self.project_name = project.get("name")
        self.project_path = self._path_or_none(project.get("path"))
        self.project_json_path = Path(project_json_path)
        self.domain_db_path = self._path_or_none(folders.get("domain_db"))
        self.meteo_db_path = self._path_or_none(folders.get("meteo_db"))
        self.run_folder_path = self._path_or_none(folders.get("run_folder"))

    def _path_or_none(self, value):
        if not value:
            return None
        return Path(value)


project_settings = ProjectSettings()
