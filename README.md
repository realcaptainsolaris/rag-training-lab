# RAG Training Lab: Acht Lernstationen

Kompaktes, deutschsprachiges Seminar-Lab für **RAG und Vektordatenbanken mit Python**. Die sieben ausführbaren Demos stammen konzeptionell aus dem größeren Buch-Lab `rag-python-lab`, verwenden aber nur einen ausgewählten Teralune-Corpus. Das vollständige MkDocs-Buch ist die unabhängige Vertiefungsreferenz.

Das Seminar verwendet **uv** für die Python-Version, virtuelle Umgebung und Paketinstallation. Ein lokal vorinstalliertes Python ist **nicht notwendig**.

## Voraussetzungen

- Windows 11 oder Linux, VS Code und die VS-Code-Extension **Python** von Microsoft.
- **uv** installiert und auf dem `PATH` (`uv --version`). Git ist optional; stattdessen das Projekt-ZIP entpacken.
- Internetzugriff auf die Paketquellen und auf die OpenAI-API. Die erste Einrichtung lädt Python 3.14 und Python-Pakete herunter.
- Schreibrechte im Projektverzeichnis. Für die API-Demos wird ein OpenAI-Schlüssel benötigt.

Python wird über `.python-version` auf **3.14** festgelegt; die Versionsvorgabe im `pyproject.toml` sowie die Paketversionen im `uv.lock` passen dazu. Die direkte Paketliste enthält bewusst **kein PyTorch und keinen lokalen Reranker**.

## Einrichtung unter Windows (PowerShell)

Im entpackten Projektordner `rag-training-lab`:

```powershell
uv --version
uv sync --locked
uv run python --version
Copy-Item .env.example .env
```

In `.env` den bereitgestellten `OPENAI_API_KEY` eintragen. **Niemals den API-Schlüssel in Git hochladen oder in Screenshots zeigen.**

Wenn Python 3.14 noch nicht vorhanden ist, lädt uv es automatisch. Falls die Unternehmens-Firewall Downloads blockiert, muss die IT den Zugriff vor Schulungsbeginn ermöglichen.

VS Code öffnen, im Projektordner mit **Python: Select Interpreter** den Interpreter `.venv\Scripts\python.exe` auswählen. Eine manuelle Aktivierung von `.venv` ist nicht erforderlich.

## Einrichtung unter Linux

```bash
uv --version
uv sync --locked
uv run python --version
cp .env.example .env
```

In `.env` den API-Schlüssel eintragen. VS-Code-Interpreter: `.venv/bin/python`.

## Erste Beispiele

Die folgenden Befehle werden **im Repository-Stammverzeichnis** ausgeführt:

```powershell
# Ohne OpenAI-Schlüssel: Chunking demonstrieren
uv run python -m stations.02_chunking

# Ohne OpenAI-Schlüssel: Zugriffskontrolle demonstrieren
uv run python -m stations.07_security

# Mit OpenAI-Schlüssel: erste RAG-Pipeline
uv run python -m stations.01_first_rag

# Chroma: einmalig Index aufbauen und anschließend suchen
uv run python -m stations.03_chroma --index
uv run python -m stations.03_chroma
```

Anschließend können die Stationen 4 bis 6 gegen den gespeicherten Index laufen.

## Lernstationen

| Station | Demo | Voraussetzung |
| --- | --- | --- |
| RAG-Grundlagen | `uv run python -m stations.01_first_rag` | API-Schlüssel |
| Dokumente und Chunking | `uv run python -m stations.02_chunking` | keine API |
| Chroma und Versionsfilter | `uv run python -m stations.03_chroma --index` und anschließend ohne `--index` | API-Schlüssel |
| Hybrid Search und RRF | `uv run python -m stations.04_hybrid` | Index und API-Schlüssel |
| Grounding und Quellen | `uv run python -m stations.05_grounding` | Index und API-Schlüssel |
| Evaluation | `uv run python -m stations.06_evaluation` | Index und API-Schlüssel |
| Rechte und Sicherheit | `uv run python -m stations.07_security` | keine API |
| Architektur und Ausblick | Folien, keine Pflicht-Demo | keine API |

Der Index muss pro Umgebung nur einmal mit `--index` erzeugt werden. Gespeicherte Dokument-Embeddings werden bei weiteren Abfragen wiederverwendet.

## Offline-Funktionstest

```powershell
uv run python -m unittest discover -s tests -v
```

Dieser Test benötigt **keinen** OpenAI-Schlüssel. Er prüft die Daten-/Evidence-Zuordnung, das beispielhafte Berechtigungsschema sowie Retrieval-Metriken und RRF. Er ersetzt **keinen** echten End-to-End-Test mit Chroma/OpenAI.

## Was die Teilnehmer ausprobieren können

- Station 1: Die Frage (`QUESTION`) ändern.
- Station 2: `CHUNK_SIZE` und `OVERLAP` variieren.
- Station 3: Versionsfilter aktivieren und vergleichen.
- Station 4: Dense Ranking, BM25 und RRF vergleichen.
- Station 5: Eine unbeantwortbare Frage stellen.
- Station 6: Goldfragen gegen den gespeicherten Index prüfen.
- Station 7: Rollen und Berechtigungsfälle diskutieren.

## Daten und Grenzen

- Der Mini-Corpus enthält 16 unveränderte Teralune-Quelldokumente (Markdown, HTML, CSV). Er enthält auch `customer`, `internal` und `restricted` Daten **ausschließlich als synthetisches Lehrmaterial**. Eine echte lokale Dateitrennung wird damit nicht sichergestellt.
- Die 15 Fragen in `data/evaluation/questions.jsonl` stammen aus dem Smoke-Test. Nur elf beantwortbare Fragen mit vollständigen Evidence-Zuordnungen fließen in Retrieval-Metriken ein. Die übrigen prüfen `deny`, `clarify` und `no_answer` getrennt.
- Ein Ranking-Score ist keine Wahrscheinlichkeit. Metadaten- und Zugriffsfilter verbessern nicht automatisch die Semantik, sondern begrenzen die zulässigen Kandidaten.
- Reranking mit einem lokalen CrossEncoder und PyTorch ist **nicht** Bestandteil dieser Schulungsinstallation.

## Installationstest und Versionsstand

Die Projektstruktur, die uv-Konfiguration und der Lockfile wurden auf Konsistenz geprüft. Der `uv.lock` verwendet die passenden, bereits im Buchprojekt festgelegten Paketversionen. Weil in dieser Entwicklungsumgebung der externe Download gesperrt und kein Python 3.14 installiert ist, wurden **weder die komplette Installation auf Windows noch API-/Chroma-End-to-End-Aufrufe verifiziert**. Diese Tests müssen auf der vorgesehenen Schulungs-VM erfolgen.

Quelldokumente und Grenzen: `QUELLEN_UND_GRENZEN.md`. Dozentennotizen: `DIDAKTIK.md`. Herkunft/Lizenz: `TERALUNE_LICENSE-CODE`.
