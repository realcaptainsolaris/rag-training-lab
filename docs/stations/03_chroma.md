# Station 03: Unsere erste Vektordatenbank mit Chroma

## Lernziel

Du lernst, wie wir Text-Chunks und ihre Embeddings dauerhaft in einer Vektordatenbank speichern und anschließend semantisch durchsuchen.

## Hintergrund

In Station 01 haben wir die Ähnlichkeit zwischen fünf Dokumenten und einer Frage selbst mit NumPy berechnet.

Bei einer größeren Wissensbasis ist dieses Vorgehen unpraktisch. Wir benötigen eine Datenbank, die Embeddings verwaltet und eine effiziente Ähnlichkeitssuche ermöglicht.

Dafür verwenden wir **Chroma**, eine Vektordatenbank, die lokal betrieben werden kann.

Chroma organisiert Einträge in sogenannten **Collections**. Eine Collection enthält unter anderem:

- eindeutige IDs
- Dokumenttexte
- Embeddings
- optional Metadaten

## Was machen wir?

### 1. Index erstellen

Wir verwenden erneut die fünf Dokumente aus Station 01.

Zunächst erzeugen wir ihre Embeddings mit `text-embedding-3-small` und speichern sie zusammen mit den Dokumenttexten und IDs in Chroma.

Diesen Vorgang nennen wir **Ingestion**.

```bash
uv run python -m stations.03_chroma --index
```

Mit `PersistentClient` werden die Daten auf der Festplatte gespeichert. Sie bleiben auch nach dem Programmende erhalten.

### 2. Semantische Suche durchführen

Anschließend starten wir das Programm ohne `--index`:

```bash
uv run python -m stations.03_chroma
```

Jetzt öffnen wir die vorhandene Collection.

Die Dokument-Embeddings müssen nicht erneut berechnet werden. Lediglich für unsere neue Frage erzeugen wir ein Embedding.

Chroma vergleicht diesen Fragevektor mit den gespeicherten Vektoren und liefert die drei nächsten Treffer zurück.

## Was zeigt der Output?

Unsere Collection enthält fünf Chunks.

Wir stellen die Frage:

```text
How long is an Orbit access token valid?
```

Chroma liefert:

| Distanz | Dokument |
|---:|---|
| **0,316** | Orbit access tokens are valid for 60 minutes. |
| 0,792 | Orbit retains telemetry data for 90 days. |
| 0,843 | Orbit limits API clients to 1000 requests per minute. |

Das richtige Dokument steht an erster Stelle.

**Wichtig:** In Station 01 haben wir Kosinusähnlichkeiten verglichen. Dort waren größere Werte besser.

Chroma liefert hier dagegen **Distanzen** zurück. Kleinere Werte bedeuten eine größere Nähe im Vektorraum.

## Ähnlichkeits- und Distanzmetriken

Vektordatenbanken unterstützen unterschiedliche Verfahren, um Embeddings zu vergleichen.

| Metrik | Bedeutung | Bester Wert |
|---|---|---|
| Cosine Similarity | Ähnlichkeit der Vektorrichtungen | Möglichst groß |
| Cosine Distance | Abstand anhand der Vektorrichtungen | Möglichst klein |
| Euclidean Distance (L2) | Räumlicher Abstand zwischen Vektoren | Möglichst klein |
| Dot Product | Skalarprodukt der Vektoren | Möglichst groß |

**Achtung:** Chroma verwendet bei neu angelegten Collections standardmäßig die quadrierte euklidische Distanz (`l2`). Unsere Ausgabe zeigt deshalb nicht automatisch eine Kosinusdistanz.

Für normierte Embeddings liefern diese Verfahren dieselbe Rangfolge, ihre Zahlenwerte unterscheiden sich jedoch.

Welche Metrik geeignet ist, hängt insbesondere vom verwendeten Embedding-Modell ab.

## Warum ist das für RAG wichtig?

Mit Chroma haben wir zwei Verarbeitungsschritte voneinander getrennt:

**Ingestion:** Dokumente vorbereiten, Embeddings erzeugen und dauerhaft speichern.

**Retrieval:** Eine Frage einbetten und passende Dokumente aus der bestehenden Datenbank abrufen.

Dadurch müssen wir nicht bei jeder Benutzerfrage sämtliche Dokumente erneut vektorisieren.

Bei großen Datenbeständen ermöglichen spezialisierte Suchindizes außerdem eine effizientere Suche als der vollständige Vergleich mit jedem gespeicherten Vektor.

## Eigenes Experiment

Ändere die Frage im Skript und führe die Suche erneut aus.

Beobachte, wie sich die Reihenfolge und die Distanzen der Treffer verändern.

Starte das Programm außerdem mehrfach ohne `--index`. Die gespeicherten Dokumente bleiben erhalten.

## Merksatz

**Eine Vektordatenbank speichert Embeddings dauerhaft und ermöglicht die semantische Suche. Die Dokumente werden bei der Ingestion eingebettet, bei einer Suchanfrage nur noch die Frage.**
