# Station 05: Metadaten und Versionsfilter in Chroma

## Lernziel

Du lernst, wie wir Dokumente mit Metadaten versehen und diese Informationen verwenden, um eine semantische Suche gezielt einzuschränken.

## Hintergrund

In Station 04 haben wir ein Problem entdeckt:

Unsere Vektorsuche lieferte für die Frage nach der Gültigkeit eines Access Tokens zuerst ein historisches Dokument.

Orbit 2.4: **120 Minuten**

Orbit 3.0: **60 Minuten**

Der historische Text war semantisch relevant, aber für die aktuelle Produktversion nicht gültig.

Um solche Probleme zu vermeiden, benötigen wir zusätzliche Informationen über unsere Dokumente.

Diese Informationen nennen wir **Metadaten**.

## Was machen wir?

### 1. Metadaten aus dem Manifest lesen

Unser Teralune-Korpus enthält eine Datei namens `manifest.json`.

Darin stehen Informationen über die einzelnen Dokumente, beispielsweise:

```json
{
    "id": "D004",
    "version": "2.4",
    "status": "historical"
}
```

Wir übernehmen ausgewählte Eigenschaften als Metadaten für jeden Chunk.

Die Metadaten werden in Chroma separat vom Text und vom Embedding gespeichert.

Das ist wichtig: **Ein Metadatenfilter vergleicht strukturierte Werte. Er führt keine semantische Suche über diese Werte durch.**

### 2. Dokumente mit Metadaten indexieren

Wir erweitern unsere bekannte Ingestion-Pipeline:

```text
Markdown-Dokumente       manifest.json
        |                      |
        v                      v
  Structure Chunking       Metadaten
        |                      |
        +----------+-----------+
                   |
                   v
            Chroma-Collection
                   |
          Texte + Embeddings
              + Metadaten
```

Die Indexierung starten wir mit:

```bash
uv run python -m stations.05_chroma_filter --index
```

Die bekannte Indexierungslogik ist jetzt in der Funktion `build_index()` zusammengefasst.

### 3. Suche mit und ohne Filter vergleichen

Anschließend starten wir:

```bash
uv run python -m stations.05_chroma_filter
```

Wir führen zwei Suchanfragen mit demselben Frage-Embedding durch.

Zuerst durchsuchen wir sämtliche Dokumente.

Danach beschränken wir die Suche mithilfe des Chroma-Parameters `where` auf eine bestimmte Produktversion.

Innerhalb der gefilterten Dokumentmenge erfolgt weiterhin eine semantische Suche.

## Was zeigt der Output?

Unsere Collection enthält **42 Chunks**.

Die Frage lautet:

> How long is an Orbit 3 access token valid?

### Suche ohne Filter

| Rang | Quelle | Version | Distanz | Information |
|---|---|---|---:|---|
| 1 | D004.md | 2.4 | **0,686** | 120 Minuten |
| 2 | D033.md | 3.0 | 0,741 | 60 Minuten |
| 3 | D002.md | 3.0 | 0,775 | 60 Minuten |

Obwohl die Frage ausdrücklich Orbit 3 erwähnt, steht das historische Dokument mit Version 2.4 auf Rang 1.

### Suche mit Versionsfilter

| Rang | Quelle | Version | Distanz | Information |
|---|---|---|---:|---|
| 1 | D033.md | 3.0 | **0,741** | 60 Minuten |
| 2 | D002.md | 3.0 | 0,775 | 60 Minuten |
| 3 | D005.md | 3.0 | 0,886 | 60 Minuten |

Der historische Treffer ist verschwunden.

**Beobachtung:** Die Distanzen der verbleibenden Dokumente ändern sich nicht. Der Filter verändert nicht die Embeddings, sondern schränkt die Menge der zulässigen Treffer ein.

## Warum ist das für RAG wichtig?

Metadatenfilter ermöglichen es, fachliche Anforderungen mit semantischer Suche zu kombinieren.

Beispielsweise können wir Dokumente anhand ihrer Produktversion, ihres Freigabestatus oder ihrer Zugriffsklasse auswählen.

Allerdings garantiert ein Versionsfilter allein noch keine zuverlässige Information.

Ein Dokument kann zur richtigen Version gehören und trotzdem den Status `unreviewed` besitzen.

In produktiven RAG-Systemen werden deshalb häufig mehrere Bedingungen kombiniert.

## Eigenes Experiment

Verändere:

```python
FILTER_VERSION = "2.4"
```

Führe die Suche erneut aus und vergleiche die Treffer mit Version 3.0.

Überlege außerdem, welche zusätzlichen Metadaten für ein unternehmensinternes RAG-System sinnvoll wären.

