# memory/storage.py

import json
import os

class Memory:
    def __init__(self, filename="knowledge_base.json"):
        self.filename = os.path.join("memory", filename)
        self.knowledge = self._load()
    
    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {"language_rules": {}} # Startet mit leeren Regeln

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.knowledge, f, indent=4)
            
    def get_rules(self):
        # Gibt die Regeln für den DependencyAnalyzerAgent zurück
        return self.knowledge.get("language_rules", {})

    def add_rule(self, lang, manifest, pattern):
        # Fügt eine neue Sprache zur Konfiguration hinzu
        self.knowledge["language_rules"][lang] = {
            "manifest": manifest,
            "pattern": pattern
        }
        self.save()

# Dieses Modul würde später mit einer Vektor-DB erweitert werden.