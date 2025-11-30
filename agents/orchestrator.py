# agents/orchestrator.py

import os
import google.generativeai as genai
from .dependency_analyzer import DependencyAnalyzerAgent
from .documentation_manager import DocumentationAgent
from .qa_manager import QualityAssuranceAgent
from memory.storage import Memory

class ProjectOrchestratorAgent:
    def __init__(self, memory_system: Memory):
        self.memory = memory_system
        self.dependency_agent = DependencyAnalyzerAgent(memory_system)
        self.documentation_agent = DocumentationAgent(memory_system)
        self.qa_agent = QualityAssuranceAgent(memory_system)
        
        # Gemini API-Initialisierung
        # HINWEIS: Der GEMINI_API_KEY muss als Umgebungsvariable gesetzt sein.
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                print("Warnung: GEMINI_API_KEY Umgebungsvariable nicht gefunden. Gemini-Funktionen sind deaktiviert.")
                self.gemini_client = None
            else:
                genai.configure(api_key=api_key)
                self.gemini_client = genai.GenerativeModel('gemini-pro')
                print("Gemini-Client erfolgreich initialisiert.")
        except Exception as e:
            print(f"Fehler bei der Initialisierung des Gemini-Clients: {e}")
            self.gemini_client = None

        print("Orchestrator initialisiert und Sub-Agenten geladen.")
        
    def init_project(self, project_path: str):
        """Initialisiert und analysiert ein neues Projekt."""
        print(f"Orchestrator startet Initialisierung für: {project_path}")
        
        # 1. Analyse durchführen
        if not self.dependency_agent.analyze_project(project_path):
            print("Fehler: Die Projekanalyse konnte nicht erfolgreich durchgeführt werden.")
            return

        # 2. QA-Schritt 1: Überprüfen, ob die Analyse Ergebnisse geliefert hat
        found_dependencies = self.dependency_agent.get_found_dependencies()
        if not self.qa_agent.verify_analysis_has_results(found_dependencies):
            print("Info: Keine Abhängigkeiten gefunden, für die Manifeste erstellt werden könnten. Prozess beendet.")
            return
        print("QA (Analyse): Prüfung der Analyseergebnisse erfolgreich.")

        # 3. Manifest-Dateien erstellen
        self.dependency_agent.create_manifests(project_path)

        # 4. QA-Schritt 2: Überprüfen, ob die Manifest-Dateien erstellt wurden
        rules = self.memory.get_rules()
        for lang in found_dependencies:
            manifest_filename = rules[lang]["manifest"]
            manifest_path = os.path.join(project_path, manifest_filename)
            if not self.qa_agent.verify_file_exists(manifest_path):
                print(f"Fehler: QA-Prüfung für erstellte Manifest-Datei '{manifest_path}' fehlgeschlagen. Prozess wird gestoppt.")
                return
        print("QA (Manifests): Prüfung der erstellten Manifest-Dateien erfolgreich.")

        print("\nProjekt-Initialisierung erfolgreich abgeschlossen.")
        # Zukünftige Schritte...
        # self.documentation_agent.update_readme(project_path, "Initialisierung abgeschlossen.")

    def add_language_rule(self, lang: str, manifest: str, pattern: str):
        """Fügt eine neue Sprache zur Konfiguration hinzu."""
        print(f"Füge neue Regel für {lang} hinzu (Manifest: {manifest}, Muster: {pattern})")
        self.memory.add_rule(lang, manifest, pattern)
        print("Regel erfolgreich im Langzeitgedächtnis gespeichert.")