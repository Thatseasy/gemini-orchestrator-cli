# cli.py

import argparse
import os
from agents.orchestrator import ProjectOrchestratorAgent
from memory.storage import Memory

def main():
    parser = argparse.ArgumentParser(description="Gemini Projekt-Orchestrator CLI")
    subparsers = parser.add_subparsers(dest="command")

    # --- Initialisierungs-Befehl (init) ---
    init_parser = subparsers.add_parser('init', help='Initialisiert und analysiert ein Projekt.')
    init_parser.add_argument('--path', type=str, required=True, help='Pfad zum Projektordner.')
    
    # --- Konfigurations-Befehl (config add-lang) ---
    config_parser = subparsers.add_parser('config', help='Verwaltet die Agenten-Konfiguration.')
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    
    add_lang_parser = config_subparsers.add_parser('add-lang', help='Fügt eine neue Sprache zur Abhängigkeitserkennung hinzu.')
    add_lang_parser.add_argument('--lang', type=str, required=True, help='Name der Programmiersprache (z.B. rust).')
    add_lang_parser.add_argument('--manifest', type=str, required=True, help='Name der Manifest-Datei (z.B. Cargo.toml).')
    add_lang_parser.add_argument('--pattern', type=str, required=True, help='Regulärer Ausdruck zur Erkennung von Abhängigkeiten im Code.')
    
    args = parser.parse_args()
    
    # Initialisiere Gedächtnis und Master-Agent
    memory_system = Memory()
    orchestrator = ProjectOrchestratorAgent(memory_system)

    if args.command == 'init':
        # Überprüfe, ob der Pfad existiert
        if not os.path.isdir(args.path):
            print(f"Fehler: Pfad {args.path} existiert nicht oder ist kein Ordner.")
            return
        orchestrator.init_project(args.path)
        
    elif args.config_command == 'add-lang':
        orchestrator.add_language_rule(args.lang, args.manifest, args.pattern)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()