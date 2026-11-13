# Station 08: Hybrid Search mit BM25 und Dense Retrieval

## Lernziel

Du lernst, wie wir lexikalische und semantische Suche kombinieren, um die Stärken beider Verfahren zu nutzen.

## Hintergrund

In den letzten Stationen haben wir drei Verfahren kennengelernt:

1. **Dense Retrieval:** Findet semantisch ähnliche Texte anhand von Embeddings.
2. **BM25:** Findet Dokumente anhand ihrer Suchbegriffe.
3. **Reciprocal Rank Fusion (RRF):** Kombiniert mehrere Rankings anhand ihrer Rangpositionen.

Jetzt verbinden wir diese Verfahren zu einer gemeinsamen Suchpipeline.

Diesen Ansatz nennen wir **Hybrid Search**.

## Was machen wir?

Unsere Pipeline besteht aus drei Schritten:

```text
                  Suchfrage
                      |
             +--------+--------+
             |                 |
             v                 v
            BM25         Dense Retrieval
             |                 |
             v                 v
       BM25-Ranking       Dense-Ranking
             |                 |
             +--------+--------+
                      |
                      v
                     RRF
                      |
                      v
               Hybrid-Ranking
```

### 1. Lexikalische Suche

Wir laden die 42 Chunks aus unserer Chroma-Collection und berechnen mit BM25 ein Ranking anhand der Suchbegriffe.

### 2. Semantische Suche

Wir erzeugen ein Embedding für die Suchfrage und suchen mit Chroma nach ähnlichen Dokumentvektoren.

### 3. Rankings kombinieren

RRF kombiniert die beiden Ergebnislisten.

Dabei werden nicht die ursprünglichen BM25-Scores und Vektordistanzen addiert.

Stattdessen erhält jeder Chunk Punkte entsprechend seiner Position in den beiden Rankings.

Ein Chunk, der in beiden Rankings vorkommt, erhält Beiträge aus beiden Listen.

## Was zeigt der Output?

### Frage 1: Wie lange ist ein Cursor gültig?

```text
How long does a cursor remain valid?
```

Die drei Rankings im Vergleich:

| Rang | BM25 | Dense Retrieval | Hybrid Search |
|---|---|---|---|
| 1 | **D022_2** | **D022_2** | **D022_2** |
| 2 | D022_5 | D022_1 | D022_1 |
| 3 | D005_1 | D022_0 | D022_5 |

Beide Suchverfahren finden denselben besten Treffer.

Chunk `D022_2` enthält die gesuchte Information: Ein Cursor ist 15 Minuten gültig.

Da beide Verfahren diesen Chunk auf Rang 1 platzieren, erhält er auch den höchsten RRF-Score.

### Frage 2: Suche nach einem technischen Bezeichner

```text
next_cursor
```

Jetzt unterscheiden sich die Ergebnisse:

| Rang | BM25 | Dense Retrieval | Hybrid Search |
|---|---|---|---|
| 1 | **D022_1** | D022_0 | **D022_1** |
| 2 | | D022_1 | D022_0 |
| 3 | | D022_2 | D022_2 |

BM25 findet nur einen Treffer mit positivem Score: `D022_1`.

Dense Retrieval setzt dagegen `D022_0` auf den ersten Platz.

**Warum gewinnt bei Hybrid Search trotzdem D022_1?**

Der Chunk erhält Punkte aus beiden Rankings:

```text
BM25:  Rang 1
Dense: Rang 2

RRF = 1/61 + 1/62
    = 0,03252
```

Chunk `D022_0` erhält dagegen nur Punkte aus dem Dense-Ranking.

Dadurch gewinnt `D022_1` das kombinierte Ranking.

Das Beispiel zeigt, wie ein exakter lexikalischer Treffer durch die Kombination beider Verfahren aufgewertet werden kann.

## Warum ist das für RAG wichtig?

Hybrid Search kann unterschiedliche Arten von Suchfragen besser abdecken.

Bei natürlich formulierten Fragen ist häufig die semantische Ähnlichkeit entscheidend.

Bei Fehlercodes, Produktnummern oder API-Bezeichnern können exakte Suchbegriffe besonders wichtig sein.

Durch die Kombination beider Verfahren müssen wir uns nicht grundsätzlich für einen einzigen Suchansatz entscheiden.

Allerdings gilt:

**Hybrid Search garantiert nicht automatisch bessere Ergebnisse.**

Ob die Kombination tatsächlich Vorteile bringt, müssen wir anhand geeigneter Testfragen überprüfen.

## Eigenes Experiment

Verändere die Suchfragen und vergleiche die drei Rankings.

Achte besonders darauf, bei welchen Fragen BM25 und Dense Retrieval unterschiedliche Treffer bevorzugen.

Überlege, warum das kombinierte Ranking bestimmte Chunks höher bewertet.

## Merksatz

**Hybrid Search kombiniert lexikalische und semantische Suche. RRF führt die unterschiedlichen Rankings zusammen, ohne ihre ursprünglichen Scores direkt vergleichen zu müssen.**
