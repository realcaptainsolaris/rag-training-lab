# RAG Training Lab

Dieses Repository begleitet die Schulung **„RAG und Vektordatenbanken mit Python“**. Es enthält sieben kleine, ausführbare Experimente zu Retrieval-Augmented Generation (RAG). Wir arbeiten mit einem fiktiven Dokumentbestand rund um **Teralune Orbit** und bauen die Konzepte Schritt für Schritt auf.

Die Beispiele sollen Mechanismen sichtbar machen und zum Experimentieren einladen. Sie sind **keine produktionsreife RAG-Anwendung**. Fachliche Vertiefungen stehen im begleitenden PDF-E-Book *Einführung in RAG mit Python*.

## Voraussetzungen

- Windows 11 oder Linux, empfohlen mit **VS Code** und der Python-Erweiterung.
- **uv** für Python, virtuelle Umgebung und Projektabhängigkeiten (`uv --version`).
- Das vollständige Schulungs-Repository einschließlich des Verzeichnisses `data/`.
- Internetzugang für die erstmalige Einrichtung und für die OpenAI-API.
- Ein bereitgestellter **OpenAI-API-Schlüssel** für die API-basierten Experimente.

Python muss nicht separat installiert sein: uv kann die im Projekt festgelegte Version **Python 3.14** herunterladen. Die Abhängigkeiten sind in `pyproject.toml` und `uv.lock` festgelegt. Für die Übungen wird **keine GPU** benötigt.

## Einrichtung

Repository klonen oder als ZIP entpacken, dann im **Projektverzeichnis** PowerShell öffnen:

```powershell
uv sync --locked
uv run python --version
Copy-Item env.example .env
```

In der neu angelegten `.env` den bereitgestellten API-Schlüssel eintragen:

```dotenv
OPENAI_API_KEY=HIER_DEN_EIGENEN_SCHLUESSEL_EINTRAGEN
CHAT_MODEL=gpt-4.1-mini
EMBEDDING_MODEL=text-embedding-3-small
```

**API-Schlüssel niemals in Git hochladen oder in Screenshots zeigen.** Die Datei `env.example` ist nur eine Vorlage; ihre Beispielwerte sind keine gültigen Zugangsdaten.

Unter Linux lautet der Kopierbefehl `cp env.example .env`; die übrigen uv-Befehle sind identisch. In VS Code kann als Interpreter unter Windows `.venv\Scripts\python.exe` beziehungsweise unter Linux `.venv/bin/python` ausgewählt werden. Eine manuelle Aktivierung der virtuellen Umgebung ist nicht notwendig.

## Schnellstart

Alle Befehle werden im **Stammverzeichnis des Repositories** ausgeführt.

**Ohne API-Schlüssel** kannst du sofort Chunking und das Berechtigungsbeispiel ansehen:

```powershell
uv run python -m stations.02_chunking
uv run python -m stations.07_security
```

**Mit API-Schlüssel** startest du die erste RAG-Demo und baust anschließend den lokalen Chroma-Index auf:

```powershell
uv run python -m stations.01_first_rag
uv run python -m stations.03_chroma --index
uv run python -m stations.03_chroma
```

`--index` erzeugt die Dokument-Embeddings und speichert sie persistent unter `data/chroma/`. Der zweite Chroma-Aufruf verwendet den bestehenden Index. **Stationen 4 bis 6 benötigen den zuvor aufgebauten Index.**

## Die acht Lernstationen

| Station | Thema und Lernziel | Experiment | Benötigt |
| --- | --- | --- | --- |
| 1 | **RAG-Grundlagen:** Retrieval und Antwortgenerierung unterscheiden, Scores richtig einordnen | `stations.01_first_rag` | API |
| 2 | **Dokumentverarbeitung und Chunking:** Fixed Size, Overlap und Struktur vergleichen | `stations.02_chunking` | Dokumentdaten |
| 3 | **Embeddings und Vektordatenbanken:** Chroma-Persistenz, semantische Suche und Versionsfilter beobachten | `stations.03_chroma` | API; beim ersten Mal `--index` |
| 4 | **Retrieval-Strategien:** Dense Retrieval, BM25 und Reciprocal Rank Fusion (RRF) vergleichen | `stations.04_hybrid` | API und Index |
| 5 | **Context Engineering und Grounding:** Quellenbezug und fehlende Evidenz untersuchen | `stations.05_grounding` | API und Index |
| 6 | **Evaluation und Fehlerdiagnose:** Hit@k, Precision@k, Recall@k und MRR interpretieren | `stations.06_evaluation` | API und Index |
| 7 | **Sicherheit und Zugriffskontrolle:** Berechtigungen anhand von Rollen und Organisationen nachvollziehen | `stations.07_security` | Dokumentdaten; keine API |
| 8 | **Erweiterte RAG-Architekturen:** Agentic RAG, GraphRAG und Multimodal RAG einordnen | Konzeptteil der Schulung | Kein ausführbares Lab in dieser Version |

Die Aufrufe für Stationen 4 bis 6:

```powershell
uv run python -m stations.04_hybrid
uv run python -m stations.05_grounding
uv run python -m stations.06_evaluation
```

## Was du selbst ausprobieren kannst

| Station | Experimentieridee |
| --- | --- |
| 1 | Die Frage ändern und Retrieval-Treffer mit der generierten Antwort vergleichen. |
| 2 | `CHUNK_SIZE` und `OVERLAP` variieren; prüfen, ob wichtige Überschriften erhalten bleiben. |
| 3 | Treffer mit und ohne Versionsfilter vergleichen. |
| 4 | Dieselbe Frage mit Dense Retrieval und BM25 untersuchen; danach das RRF-Ranking betrachten. |
| 5 | Eine Frage stellen, die der bereitgestellte Kontext nicht beantworten kann. |
| 6 | Goldfragen und gefundene Chunks vergleichen; die vier Metriken interpretieren. |
| 7 | Die Berechtigungsmatrix für verschiedene Benutzerrollen und Organisationen analysieren. |

## Ergebnisse richtig interpretieren

**Retrieval-Scores sind keine Wahrscheinlichkeiten.** Ein hoher Score oder eine geringe Distanz beweist weder die Korrektheit eines Dokuments noch die Richtigkeit der späteren Antwort.

**Chunking beeinflusst, welche Informationen auffindbar sind.** Unterschiedliche Chunk-Grenzen bedeuten nicht automatisch, dass eine Strategie insgesamt besser ist. Das muss anhand von Testfragen untersucht werden.

**Metadatenfilter sind regelbasiert.** Ein Versionsfilter schließt zum Beispiel historische Dokumente aus, erhöht aber nicht die semantische Ähnlichkeit der verbleibenden Treffer.

**Quellenangaben sind keine Wahrheitsgarantie.** Eine Antwort kann ihrem Kontext treu sein und trotzdem einen Fehler enthalten, wenn die Quelle falsch oder veraltet ist. Ebenso garantiert ein entsprechender Prompt keine Faktentreue.

**Retrieval-Evaluation ist nicht Antwort-Evaluation.** Die Metriken der Station 6 vergleichen gefundene Chunks mit einem vorbereiteten Goldset. Das kleine Testset ist kein unabhängiger wissenschaftlicher Benchmark. Die Fragen mit den erwarteten Verhaltensweisen `clarify`, `deny` und `no_answer` werden nicht wie normale beantwortbare Retrieval-Fragen bewertet.

**Die ACL-Demo ist ein Lehrbeispiel.** Sie zeigt Berechtigungsentscheidungen, aber keine vollständige, sicher betriebene Zugriffskontrolle. In produktiven Anwendungen müssen Rechte serverseitig durchgesetzt werden. Die mitgelieferten synthetischen Dokumente sind im Schulungsprojekt lokal zugänglich.

## Offline-Tests

Die grundlegenden Tests benötigen keinen OpenAI-Schlüssel:

```powershell
uv run python -m unittest discover -s tests -v
```

Sie prüfen lokale Daten- und Evidence-Zuordnungen, Berechtigungsregeln und Retrieval-Metriken. Sie ersetzen keinen End-to-End-Test der API- und Chroma-Pipeline.

## Daten und weiterführende Informationen

Der Schulungs-Corpus enthält **16 fiktive Quelldokumente** in Markdown, HTML und CSV sowie **15 Testfragen**. Für **11 beantwortbare Testfragen** sind quantitative Retrieval-Bewertungen vorgesehen; weitere Fälle untersuchen beispielsweise Rückfragen oder Zugriffsverweigerung. Die Dokumente enthalten bewusst unterschiedliche Versionen und Zugriffsklassen.

Weitere Details zu Datenherkunft, synthetischen Inhalten und Grenzen des Beispiels stehen in [`QUELLEN_UND_GRENZEN.md`](QUELLEN_UND_GRENZEN.md). Hinweise zur Herkunft und Lizenz enthält `TERALUNE_LICENSE-CODE`.

Die vollständige fachliche Erläuterung findest du im begleitenden **PDF-E-Book „Einführung in RAG mit Python“**.
