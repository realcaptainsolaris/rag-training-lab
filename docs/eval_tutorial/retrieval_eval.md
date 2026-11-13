# Retrieval-Evaluation: Hit@k, Precision@k, Recall@k und MRR

## Lernziel

Du lernst, wie wir die Qualität eines Retrievers anhand eines Goldsets messen.

Dazu berechnen und interpretieren wir vier wichtige Retrieval-Metriken:

1. **Hit@k:** Wurde mindestens ein relevanter Chunk gefunden?
2. **Precision@k:** Wie viele der gefundenen Chunks sind relevant?
3. **Recall@k:** Wie viele der bekannten relevanten Chunks wurden gefunden?
4. **MRR@k:** Wie weit vorne steht der erste relevante Treffer?

## Hintergrund

Bisher haben wir die Ergebnisse unserer Vektorsuche hauptsächlich manuell betrachtet.

Wir haben überprüft, ob die gefundenen Chunks zur Frage passen und ob ihre Informationen für die Antwortgenerierung geeignet sind.

Für eine systematische Evaluation benötigen wir jedoch messbare Kriterien.

Dazu verwenden wir unser **Goldset** aus `goldset.json`.

Es enthält fünf Testfragen mit erwarteten Antworten und den zugehörigen Gold-Chunks.

Die Gold-Chunks sind unsere Referenz: Sie legen fest, welche Chunks für eine bestimmte Frage als relevant gelten.

## Was machen wir?

Wir simulieren die Ergebnisse eines Retrievers für fünf Goldfragen.

Dabei betrachten wir jeweils die ersten drei Suchergebnisse (`k = 3`).

**Wichtig:** Wir verwenden bewusst vorbereitete Rankings und keine echten Chroma-Suchergebnisse. So können wir die Metriken unabhängig von der Vektorsuche untersuchen.

### 1. Gefundene Chunks mit Gold-Chunks vergleichen

Für jede Frage vergleichen wir die gefundenen Chunk-IDs mit den relevanten Gold-Chunks.

Beispiel für die Frage `Q001`:

> How long is an Orbit 3.0 access token valid?

Gold-Antwort:

> 60 minutes

Relevante Gold-Chunks:

```text
D002_1
D005_1
D033_1
```

Unser simulierter Retriever liefert:

| Rang | Chunk-ID | Relevant? |
|---|---|---|
| 1 | D004_2 | Nein |
| 2 | D033_1 | Ja |
| 3 | D002_1 | Ja |

Zwei der drei gefundenen Chunks sind relevant.

Allerdings steht auf Rang 1 ein irrelevanter Chunk aus der historischen Produktversion Orbit 2.4.

### 2. Retrieval-Metriken berechnen

Aus diesem Ranking berechnen wir vier Metriken.

**Hit@3**

Mindestens ein relevanter Chunk wurde gefunden.

```text
Hit@3 = 1
```

**Precision@3**

Zwei der drei gefundenen Chunks sind relevant.

```text
Precision@3 = 2 / 3 = 0,667
```

**Recall@3**

Insgesamt existieren drei Gold-Chunks. Zwei davon wurden gefunden.

```text
Recall@3 = 2 / 3 = 0,667
```

**Reciprocal Rank (RR@3)**

Der erste relevante Chunk steht auf Rang 2.

```text
RR@3 = 1 / 2 = 0,500
```

Für jede Frage berechnen wir einen eigenen Reciprocal Rank.

Der Mittelwert über alle Fragen ergibt anschließend den **Mean Reciprocal Rank (MRR@3)**.

## Was zeigt der Output?

Starte das Programm:

```bash
uv run python -m eval_tutorial.retrieval_eval
```

Das Programm bewertet alle fünf Goldfragen.

### Ergebnisse der einzelnen Fragen

| Frage | Hit@3 | Precision@3 | Recall@3 | RR@3 |
|---|---:|---:|---:|---:|
| Q001 | 1 | 0,667 | 0,667 | 0,500 |
| Q002 | 1 | 0,333 | 0,333 | 0,333 |
| Q003 | 1 | 0,333 | 1,000 | 0,333 |
| Q004 | 1 | 0,333 | 1,000 | 0,333 |
| Q005 | 1 | 0,667 | 1,000 | 0,500 |

Bei allen fünf Fragen wurde mindestens ein relevanter Chunk gefunden.

Deshalb beträgt Hit@3 für jede Frage 1.

Die anderen Metriken unterscheiden sich jedoch deutlich.

### Gesamtergebnis

Das Programm berechnet die Mittelwerte über alle fünf Fragen:

```text
GESAMTERGEBNIS
Goldfragen:       5
Mean Hit@3:       1.000
Mean Precision@3: 0.467
Mean Recall@3:    0.800
MRR@3:            0.400
```

**Mean Hit@3 = 1,000**

Bei jeder Frage wurde mindestens ein relevanter Chunk gefunden.

**Mean Precision@3 = 0,467**

Im Durchschnitt sind nur etwa 47 % der zurückgegebenen Chunks relevant.

**Mean Recall@3 = 0,800**

Im Durchschnitt wurden 80 % der bekannten relevanten Chunks pro Frage gefunden.

**MRR@3 = 0,400**

Der erste relevante Treffer erscheint häufig erst auf Rang 2 oder 3.

## Warum ist das für RAG wichtig?

Unser Retriever erreicht einen perfekten Hit@3-Wert.

Trotzdem zeigt die Evaluation deutliche Schwächen.

Die Precision ist relativ niedrig. Das bedeutet, dass viele irrelevante Chunks in den Kontext gelangen würden.

Außerdem erscheinen relevante Informationen häufig nicht an erster Stelle.

Das kann die spätere Antwortgenerierung erschweren.

Besonders interessant ist Frage `Q003`:

Hier existiert nur ein Gold-Chunk. Dieser wird auf Rang 3 gefunden.

Deshalb erhalten wir:

```text
Hit@3       = 1,000
Precision@3 = 0,333
Recall@3    = 1,000
RR@3        = 0,333
```

Der Retriever hat alle bekannten relevanten Chunks gefunden, aber zwei der drei Suchergebnisse sind irrelevant.

**Ein hoher Recall bedeutet deshalb nicht automatisch eine hohe Precision.**

Auch ein perfekter Hit@k-Wert garantiert keine gute Reihenfolge der Suchergebnisse.

## Eigenes Experiment

Verändere die simulierten Rankings in `retrieval_eval.py`.

Setze beispielsweise bei `Q001` den Chunk `D033_1` auf Rang 1.

Führe die Evaluation erneut aus.

Beobachte, welche Metriken sich verändern.

Untersuche anschließend folgende Situationen:

1. Alle relevanten Chunks stehen auf den ersten Rängen.
2. Der einzige relevante Chunk steht auf Rang 3.
3. Unter den ersten drei Treffern befindet sich kein relevanter Chunk.

Vergleiche insbesondere Hit@3 und RR@3.

Überlege, welche Metrik die Veränderung der Trefferreihenfolge berücksichtigt.

## Merksatz

**Hit@k misst, ob mindestens ein relevanter Chunk gefunden wurde. Precision@k und Recall@k messen die Relevanz und Vollständigkeit der Treffer. MRR@k berücksichtigt zusätzlich die Position des ersten relevanten Treffers.**

Erst die gemeinsame Betrachtung dieser Metriken ermöglicht eine differenzierte Bewertung der Retrieval-Qualität.
