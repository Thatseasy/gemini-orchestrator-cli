# agents/dependency_analyzer.py

import os
import re
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from memory.storage import Memory

class DependencyAnalyzerAgent:
    """
    Ein Agent, der für die Analyse von Projekt-Abhängigkeiten zuständig ist.
    Erkennt Programmiersprachen, scannt den Code nach Abhängigkeiten und
    kann Manifest-Dateien erstellen.
    """

    def __init__(self, memory_system: 'Memory'):
        """
        Initialisiert den DependencyAnalyzerAgent.

        Args:
            memory_system: Das zentrale Gedächtnissystem des Orchestrators.
        """
        self.memory = memory_system
        self.rules = self.memory.get_rules()
        self.found_dependencies: Dict[str, List[str]] = {}

    def analyze_project(self, path: str) -> bool:
        """
        Analysiert den Projektordner rekursiv, um Abhängigkeiten zu finden.

        Args:
            path: Der Pfad zum Projektordner.

        Returns:
            True, wenn die Analyse erfolgreich war, sonst False.
        """
        print(f"-> Analysiere Projektordner: {path}")
        if not self.rules:
            print("   Warnung: Keine Sprachregeln im Gedächtnis gefunden.")
            return False

        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    for lang, rule_data in self.rules.items():
                        pattern = rule_data.get("pattern")
                        if not pattern:
                            continue

                        dependencies = re.findall(pattern, content)
                        if dependencies:
                            if lang not in self.found_dependencies:
                                self.found_dependencies[lang] = []
                            
                            # Füge nur neue Abhängigkeiten hinzu
                            for dep in dependencies:
                                if dep not in self.found_dependencies[lang]:
                                    self.found_dependencies[lang].append(dep)
                                    print(f"   - Abhängigkeit für '{lang}' gefunden: {dep} in {file}")

                except Exception as e:
                    print(f"   Fehler beim Lesen der Datei {file_path}: {e}")
        
        if not self.found_dependencies:
            print("-> Keine Abhängigkeiten nach Analyse gefunden.")
        else:
            print("-> Analyse abgeschlossen. Gefundene Abhängigkeiten:")
            for lang, deps in self.found_dependencies.items():
                print(f"   - {lang}: {', '.join(deps)}")

        return True

    def create_manifests(self, project_path: str):
        """
        Erstellt die Manifest-Dateien basierend auf den gefundenen Abhängigkeiten.

        Args:
            project_path: Der Basispfad des Projekts, in dem die Dateien erstellt werden.
        """
        print("-> Erstelle Manifest-Dateien...")
        if not self.found_dependencies:
            print("   Keine Abhängigkeiten zum Schreiben in Manifest-Dateien gefunden.")
            return

        for lang, deps in self.found_dependencies.items():
            rule = self.rules.get(lang)
            if not rule or "manifest" not in rule:
                print(f"   Warnung: Keine Manifest-Regel für '{lang}' gefunden.")
                continue

            manifest_filename = rule["manifest"]
            manifest_path = os.path.join(project_path, manifest_filename)
            content = ""

            print(f"   - Schreibe Manifest für '{lang}': {manifest_path}")

            try:
                # Formatierung basierend auf dem Dateinamen
                if manifest_filename == "Cargo.toml":
                    content = "[dependencies]\n"
                    content += "\n".join([f'{dep} = "*"' for dep in deps])
                elif manifest_filename.endswith(".txt"):
                    content = "\n".join(deps)
                else: # Fallback für unbekannte Formate
                    content = "\n".join(deps)
                
                with open(manifest_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"     '{manifest_path}' erfolgreich geschrieben.")

            except Exception as e:
                print(f"     Fehler beim Schreiben der Manifest-Datei für '{lang}': {e}")

    def get_found_dependencies(self) -> Dict[str, List[str]]:
        """
        Gibt die bei der Analyse gefundenen Abhängigkeiten zurück.
        """
        return self.found_dependencies