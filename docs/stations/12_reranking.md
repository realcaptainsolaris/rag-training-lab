# Station 12: Re-Ranking mit einem Cross-Encoder

## Lernziel

Du lernst, wie ein Cross-Encoder bereits gefundene Dokumente erneut bewertet und nach ihrer geschätzten Relevanz sortiert.

Dabei vergleichen wir zwei unterschiedliche Verfahren: **Bi-Encoder und Cross-Encoder**.

## Hintergrund

Bisher haben wir Dokumente mithilfe von Embeddings gesucht.

Dabei werden die Suchfrage und die Dokumente getrennt in Vektoren umgewandelt. Anschließend vergleichen wir ihre Vektorähnlichkeit.

Dieses Prinzip bezeichnet man als **Bi-Encoder-Ansatz**.

Ein Cross-Encoder arbeitet anders: Er verarbeitet die Suchfrage und einen Dokumenttext gemeinsam.

Dadurch kann er die Beziehungen zwischen beiden Texten direkt berücksichtigen.

| Bi-Encoder | Cross-Encoder |
|---|---|
| Frage und Dokument getrennt verarbeiten | Frage und Dokument gemeinsam verarbeiten |
| Vektorähnlichkeit berechnen | Relevanz-Score berechnen |
| Effizient für große Dokumentbestände | Rechenintensiver pro Kandidat |
| Geeignet für die erste Suche | Geeignet für die anschließende Neubewertung |

Deshalb kombinieren wir beide Verfahren.

## Was machen wir?

Unsere Pipeline besteht aus zwei Suchphasen:

```text
                  Suchfrage
                      |
                      v
                Dense Retrieval
                      |
                      v
                10 Kandidaten
                      |
                      v
                 Cross-Encoder
                      |
                      v
              Neue Relevanz-Scores
                      |
                      v
               Erneut sortieren
                      |
                      v
                Top 3 Chunks
```

### 1. Kandidaten suchen

Chroma liefert zunächst die zehn ähnlichsten Chunks.

Dafür verwenden wir wie bisher OpenAI-Embeddings mit `text-embedding-3-small`.

### 2. Cross-Encoder anwenden

Wir verwenden das Modell:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

Für jeden gefundenen Chunk erstellen wir ein Paar aus Suchfrage und Dokumenttext.

Der Cross-Encoder verarbeitet diese Paare und berechnet jeweils einen Relevanz-Score.

Das Modell läuft lokal. Für das eigentliche Re-Ranking sind keine OpenAI-API-Aufrufe erforderlich.

Beim ersten Start muss das Modell allerdings heruntergeladen werden.

### 3. Ergebnisse neu sortieren

Wir ordnen jedem Chunk seinen Cross-Encoder-Score zu.

Anschließend sortieren wir die Kandidaten absteigend nach diesem Score.

Die drei bestbewerteten Chunks bilden unser neues Ranking.

## Was zeigt der Output?

Unsere Suchfrage lautet:

> How long is an Orbit 3 access token valid?

Wir kennen die korrekte Antwort bereits: **60 Minuten**.

### Vor dem Re-Ranking

Dense Retrieval liefert folgende Spitzenreiter:

| Rang | Chunk | Inhalt |
|---|---|---|
| 1 | D004_2 | Historische Token-Gültigkeit: 120 Minuten |
| 2 | D033_1 | Orbit 3.0: 60 Minuten |
| 3 | D002_1 | Orbit 3.0: 60 Minuten |

Das Problem kennen wir bereits aus Station 09.

Der historische Chunk `D004_2` steht auf Rang 1, obwohl die Frage ausdrücklich nach Orbit 3 fragt.

### Nach dem Re-Ranking

Der Cross-Encoder verändert die Reihenfolge:

| Rang | Chunk | Cross-Encoder-Score |
|---|---|---:|
| 1 | **D002_1** | 7,474 |
| 2 | D004_2 | 6,865 |
| 3 | D033_1 | 6,768 |

Jetzt steht der korrekte Chunk `D002_1` auf Rang 1.

Der Cross-Encoder bewertet diesen Text als besonders relevant für die gestellte Frage.

Das Re-Ranking hat die Position des gewünschten Chunks in unserem Beispiel verbessert.

**Aber:** Der historische Chunk `D004_2` steht weiterhin auf Rang 2.

Der Cross-Encoder erkennt also nicht zuverlässig, dass dieser Chunk für die aktuelle Produktversion ungeeignet ist.

Das ist ein wichtiger Unterschied zwischen **semantischer Relevanz** und **fachlicher Gültigkeit**.

## Wie interpretieren wir die Scores?

Der Cross-Encoder liefert beispielsweise:

```text
D002_1    Score: 7.474
D004_2    Score: 6.865
D033_1    Score: 6.768
```

Diese Werte sind keine Wahrscheinlichkeiten.

Ein Score von 7,474 bedeutet weder 747,4 % Relevanz noch eine garantierte korrekte Antwort.

Die Scores dienen hier dazu, die Kandidaten für dieselbe Frage miteinander zu vergleichen.

## Warum ist das für RAG wichtig?

Re-Ranking kann die Qualität der Dokumentenauswahl verbessern.

Gerade bei großen Dokumentbeständen ist eine zweistufige Suche sinnvoll:

Zuerst suchen wir effizient nach einer größeren Anzahl möglicher Treffer.

Anschließend bewertet ein genaueres, aber rechenintensiveres Modell diese Kandidaten erneut.

Dabei gibt es zwei wichtige Grenzen:

**1. Re-Ranking kann keine fehlenden Dokumente finden.**

Wenn ein relevanter Chunk nicht unter den ursprünglichen zehn Kandidaten vorkommt, kann der Cross-Encoder ihn nicht berücksichtigen.

**2. Re-Ranking ersetzt keine Metadatenfilter.**

Unser Beispiel zeigt, dass ein historischer Chunk trotz Re-Ranking weit oben stehen kann.

Für ein produktives RAG-System sollten wir deshalb die bereits bekannten Verfahren kombinieren:

```text
Suchfrage
    |
    v
Metadatenfilter
    |
    v
Dense Retrieval / Hybrid Search
    |
    v
Cross-Encoder Re-Ranking
    |
    v
Kontext für das LLM
```

## Eigenes Experiment

Verändere `TOP_K_RETRIEVAL` von 10 auf 3.

Vergleiche anschließend die Ergebnisse.

Untersuche außerdem, was passiert, wenn du die Suchfrage anders formulierst.

Überlege:

**Kann ein Cross-Encoder einen relevanten Chunk auf Rang 1 bringen, wenn dieser beim ursprünglichen Retrieval gar nicht gefunden wurde?**

## Merksatz

**Dense Retrieval findet effizient mögliche Kandidaten. Ein Cross-Encoder bewertet diese Kandidaten genauer und kann ihre Reihenfolge verbessern. Re-Ranking ersetzt jedoch weder gutes Retrieval noch Metadatenfilter.**
