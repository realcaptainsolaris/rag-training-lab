# Station 04: Markdown-Dokumente in Chroma speichern

## Lernziel

Du lernst, wie wir mehrere Dokumente automatisch einlesen, in Chunks zerlegen und für eine semantische Suche in Chroma speichern.

Außerdem untersuchen wir, warum ein semantisch passender Treffer nicht unbedingt die richtige Information enthält.

## Hintergrund

In Station 03 haben wir fünf kurze Texte direkt im Python-Code gespeichert.

In einem realen RAG-System stammen Informationen dagegen häufig aus Dateien, Datenbanken oder anderen externen Quellen.

Wir erweitern deshalb unsere Ingestion-Pipeline:

```text
Markdown-Dateien
       |
       v
   Einlesen
       |
       v
Structure Chunking
       |
       v
    Embeddings
       |
       v
     Chroma
```

Als Datenbasis verwenden wir die öffentlichen Markdown-Dokumente unseres fiktiven Teralune-Korpus.

## Was machen wir?

### 1. Dokumente einlesen

Wir suchen alle Markdown-Dateien im Verzeichnis:

`data/teralune-mini/corpus/public/`

Jede Datei wird vollständig eingelesen.

### 2. Dokumente in Chunks zerlegen

Wir verwenden das Structure Chunking aus Station 02.

Jede Markdown-Überschrift der Ebenen 1 bis 3 beginnt einen neuen Chunk.

Die Chunks erhalten eindeutige IDs, beispielsweise:

```text
D022.md_0
D022.md_1
D022.md_2
```

Damit können wir einzelne Chunks später eindeutig identifizieren.

### 3. Embeddings erzeugen und speichern

Für jeden Chunk erzeugen wir mit `text-embedding-3-small` einen Embedding-Vektor.

Anschließend speichern wir IDs, Texte und Vektoren in einer Chroma-Collection.

Die Indexierung starten wir mit:

```bash
uv run python -m stations.04_chroma_documents --index
```

### 4. Semantische Suche durchführen

Nach der Indexierung können wir die gespeicherten Chunks durchsuchen:

```bash
uv run python -m stations.04_chroma_documents
```

Chroma liefert die drei ähnlichsten Textabschnitte.

## Was zeigt der Output?

Unsere Collection enthält **42 Chunks**.

Wir stellen die Frage:

> How long is an Orbit access token valid?

Die Suche liefert:

| Rang | Distanz | Gefundene Information |
|---|---:|---|
| 1 | **0,696** | Orbit 2.4: 120 Minuten |
| 2 | 0,776 | Orbit 3.0: 60 Minuten |
| 3 | 0,825 | Orbit 3.0: 60 Minuten |

Das Ergebnis ist bemerkenswert.

**Der ähnlichste Chunk enthält eine veraltete Information!**

Der erste Treffer stammt aus der Dokumentation für Orbit 2.4. Dort beträgt die Gültigkeit eines Access Tokens 120 Minuten.

Für die aktuelle Version Orbit 3.0 beträgt sie jedoch 60 Minuten.

Chroma hat keinen technischen Fehler gemacht. Der erste Text ist semantisch sehr relevant für unsere Frage.

Das Problem besteht darin, dass unser Retriever bisher nicht zwischen historischen und aktuellen Dokumenten unterscheidet.

## Warum ist das für RAG wichtig?

Eine reine Vektorsuche bewertet die Ähnlichkeit zwischen Frage und Dokumenten.

Sie berücksichtigt nicht automatisch:

- ob ein Dokument aktuell oder veraltet ist
- für welche Produktversion eine Information gilt
- ob ein Dokument offiziell freigegeben wurde
- ob ein Benutzer auf die Information zugreifen darf

Ein RAG-System kann deshalb eine inhaltlich plausible, aber sachlich falsche Antwort erzeugen, obwohl die korrekte Information ebenfalls in der Datenbank vorhanden ist.

**Semantische Relevanz ist nicht gleich fachliche Gültigkeit.**

In Station 05 erweitern wir unsere Suche deshalb um Metadatenfilter.

Damit können wir beispielsweise gezielt nach Dokumenten für Orbit 3.0 suchen.

## Eigenes Experiment

Verändere die Suchfrage und vergleiche die Ergebnisse.

Beispiele:

```text
How long does Orbit retry failed webhooks?
Which export formats does Orbit support?
What is the API rate limit?
```

Achte darauf, ob die gefundenen Informationen zur aktuellen Produktversion gehören.

**Eine Vektordatenbank findet semantisch ähnliche Informationen. Ob diese Informationen aktuell, gültig oder für den Benutzer zugänglich sind, muss ein RAG-System zusätzlich berücksichtigen.**
