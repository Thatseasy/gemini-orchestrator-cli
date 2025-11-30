# agents/qa_manager.py

from pathlib import Path
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from memory.storage import Memory

class QualityAssuranceAgent:
    """
    Ein Agent, der für die Überprüfung der Code- und Projektqualität zuständig ist.
    Er kann Dateien validieren, Inhaltsprüfungen durchführen und andere QA-Aufgaben übernehmen.
    """

    def __init__(self, memory_system: 'Memory'):
        """
        Initialisiert den QualityAssuranceAgent.

        Args:
            memory_system: Das zentrale Gedächtnissystem des Orchestrators.
        """
        self.memory = memory_system

    def verify_file_exists(self, file_path: str) -> bool:
        """
        Prüft, ob eine Datei am angegebenen Pfad existiert und nicht leer ist.

        Args:
            file_path: Der Pfad zur zu überprüfenden Datei.

        Returns:
            True, wenn die Datei existiert und Inhalt hat, sonst False.
        """
        path = Path(file_path)
        if not path.is_file():
            print(f"QA-Fehler: Datei '{file_path}' existiert nicht oder ist ein Ordner.")
            return False
        
        if path.stat().st_size == 0:
            print(f"QA-Fehler: Datei '{file_path}' ist leer.")
            return False
            
        return True

    def verify_analysis_has_results(self, found_dependencies: dict) -> bool:
        """
        Prüft, ob die Abhängigkeitsanalyse Ergebnisse geliefert hat.

        Args:
            found_dependencies: Das Dictionary mit den gefundenen Abhängigkeiten.

        Returns:
            True, wenn Ergebnisse vorhanden sind, sonst False.
        """
        if not found_dependencies:
            print("QA-Fehler: Die Abhängigkeitsanalyse hat keine Ergebnisse geliefert.")
            return False
        return True

    def verify_content_contains(self, file_path: str, required_keywords: List[str]) -> bool:
        """
        Prüft, ob alle erforderlichen Schlüsselwörter in einer Datei enthalten sind.

        Args:
            file_path: Der Pfad zur zu lesenden Datei.
            required_keywords: Eine Liste von Strings, die in der Datei vorkommen müssen.

        Returns:
            True, wenn alle Schlüsselwörter gefunden wurden, sonst False.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return all(keyword in content for keyword in required_keywords)
        except FileNotFoundError:
            print(f"QA-Fehler: Datei '{file_path}' konnte nicht zum Lesen gefunden werden.")
            return False
        except Exception as e:
            print(f"QA-Fehler: Ein unerwarteter Fehler ist beim Lesen von '{file_path}' aufgetreten: {e}")
            return False