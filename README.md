# RAG Training Lab

Praxisübungen zum Seminar **Retrieval-Augmented Generation (RAG) mit Python** anhand der fiktiven Orbit-API-Plattform von Teralune.

## Schnellstart

**Voraussetzungen:** Git, [uv](https://docs.astral.sh/uv/getting-started/installation/) und ein OpenAI-API-Schlüssel. **Python muss nicht separat installiert sein.** `uv` kann die für dieses Projekt benötigte Python-Version 3.14 bereitstellen.

Öffne ein Terminal im geklonten Projektordner und führe die folgenden Schritte aus.


### 0. Repository klonen

Öffne ein Terminal (PowerShell) und klone das GitHub-Repository:

```powershell
git clone <REPOSITORY-URL>
```

Wechsle anschließend in das Projektverzeichnis:

```powershell
cd rag-training-lab
```

Alle weiteren Befehle werden in diesem Verzeichnis ausgeführt.

### 1. Python und Abhängigkeiten installieren

```powershell
uv sync
```

`uv` richtet die virtuelle Umgebung `.venv` ein und installiert die im Projekt festgelegten Abhängigkeiten. Beim ersten Start ist eine Internetverbindung erforderlich.

### 2. API-Schlüssel eintragen

Erstelle aus `env.example` eine Datei namens `.env`:

**PowerShell (Windows 11):**

```powershell
Copy-Item env.example .env
```

**Bash (Linux/macOS):**

```bash
cp env.example .env
```

Öffne `.env` in VS Code und ersetze den Platzhalter durch deinen OpenAI-API-Schlüssel:

```dotenv
OPENAI_API_KEY=sk-...
```

**Wichtig:** Die Datei `.env` enthält ein Geheimnis. Teile sie nicht und lade sie nicht in ein Git-Repository hoch. Die Übungen mit OpenAI-Aufrufen verursachen API-Kosten.

### 3. Installation prüfen

```powershell
uv run python --version
```

Erwartet wird eine Ausgabe wie:

```text
Python 3.14.x
```

Damit ist die Arbeitsumgebung vorbereitet.

## Stationen ausführen

Starte die Übungen **im Projektverzeichnis**. Jede Station ist eine eigenständige Python-Datei im Ordner `stations/`.

Beispiel:

```powershell
uv run python -m stations.00_tokens
```

Einige Stationen benötigen zuerst einen lokalen Chroma-Index. Diesen erstellst du einmalig mit `--index`:

```powershell
uv run python -m stations.05_chroma_filter --index
uv run python -m stations.05_chroma_filter
```

Die erzeugten Chroma-Datenbanken liegen lokal unter `data/chroma_*/` und werden nicht in Git gespeichert. Wenn ein Index fehlt, führe den passenden Indexierungsbefehl erneut aus.

## Übersicht der Stationen

| Station | Thema | Hinweis |
| --- | --- | --- |
| `00_tokens` | Tokenisierung | Einstieg |
| `01_first_rag` | Erste RAG-Pipeline mit Embeddings | OpenAI API |
| `02_chunking` | Texte in Chunks zerlegen | |
| `03_chroma` | Erste Vektorsuche mit Chroma | Zuerst `--index` |
| `04_chroma_documents` | Dokumente in Chroma indexieren | Zuerst `--index` |
| `05_chroma_filter` | Metadatenfilter und Versionen | Zuerst `--index` |
| `06_bm25_search` | Schlüsselwortsuche mit BM25 | Index aus Station 05 |
| `07_rrf` | Reciprocal Rank Fusion | |
| `08_hybrid_search` | Dense Search, BM25 und RRF kombinieren | Index aus Station 05 |
| `09_evaluation` | Retrieval mit Goldfragen evaluieren | Index aus Station 05 |
| `10_grounding` | Antworten auf gefundene Quellen stützen | Index aus Station 05 |
| `11_security` | Zugriffsrechte beim Retrieval | Zuerst `--index` |
| `12_reranking` | Suchergebnisse mit Cross-Encoder neu sortieren | **Optional; zusätzliche Installation** |
| `13_parsing` | HTML und CSV einlesen | |
| `14_costs` | Tokenverbrauch und API-Kosten messen | Index aus Station 05 |
| `15_multimodal` | Bilder beschreiben und semantisch suchen | Zuerst `--index` |

### Optionale Station 12: Reranking

Die Standardinstallation enthält bewusst **kein** `sentence-transformers`, da das Paket zusätzliche, umfangreiche ML-Abhängigkeiten benötigt. Station 12 kann daher erst nach einer zusätzlichen Installation ausgeführt werden:

```powershell
uv add sentence-transformers
uv run python -m stations.12_reranking
```

Das Cross-Encoder-Modell wird beim ersten Start aus dem Internet heruntergeladen. Diese Station wird nur durchgeführt, wenn im Seminar ausreichend Zeit bleibt.

## Projektstruktur

```text
rag-training-lab/
├── data/
│   ├── evaluation/          # Materialien für Evaluation
│   ├── images/              # Übungsbilder für Station 15
│   └── teralune-mini/       # Fiktiver Dokumentenkorpus
├── stations/                # Python-Übungen 00 bis 15
├── .python-version          # Python 3.14
├── env.example              # Vorlage für den API-Schlüssel
├── pyproject.toml           # Projekt und Abhängigkeiten
└── uv.lock                  # Festgelegte Paketversionen
```

## Häufige Probleme

**`uv` wird nicht erkannt:** Prüfe die [uv-Installationsanleitung](https://docs.astral.sh/uv/getting-started/installation/) und starte das Terminal nach der Installation neu.

**`OPENAI_API_KEY` fehlt:** Prüfe, ob die Datei wirklich `.env` heißt, im Projektverzeichnis liegt und einen gültigen API-Schlüssel enthält.

**Chroma-Collection nicht gefunden:** Führe zunächst die passende Station mit `--index` aus. Mehrere spätere Stationen verwenden den Index von Station 05.

**Erster Start dauert länger:** `uv` lädt bei Bedarf Python und Pakete herunter. Für die optionale Station 12 ist zusätzlich ein Modelldownload nötig.

## Hinweise

Der Teralune-/Orbit-Datenbestand ist **fiktives Schulungsmaterial**. Die Beispiele dienen dem Verständnis von Retrieval, RAG, Evaluation und Sicherheit; sie sind keine produktive API-Dokumentation.

Weitere Erklärungen erhältst du im Seminar über die Folien, die begleitenden Stationsdokumente und die Buchreferenz.
