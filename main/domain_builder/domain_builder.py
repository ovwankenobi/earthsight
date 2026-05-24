# -*- coding: utf-8 -*-
"""
Created on Sun May 24, 2026

@author: rsderamos
"""

from pathlib import Path


class DomainBuilderSettings:
    def __init__(self):
        self.clear()

    def clear(self):
        self.domain_name = None
        self.domain_path = None
        self.domain_json_path = None
        self.model_settings = {}

    def register_domain(self, domain_config, domain_json_path):
        domain = domain_config.get("domain", {})

        self.domain_name = domain.get("name")
        self.domain_path = domain.get("path")
        self.domain_json_path = Path(domain_json_path)
        self.model_settings = domain_config.get("model_settings", {})


domain_builder_settings = DomainBuilderSettings()
