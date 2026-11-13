# Station 07: Reciprocal Rank Fusion (RRF)

## Lernziel

Du lernst, wie sich zwei unterschiedliche Suchrankings zu einer gemeinsamen Ergebnisliste kombinieren lassen.

## Hintergrund

In den bisherigen Stationen haben wir zwei Suchverfahren kennengelernt:

- **Dense Retrieval:** Sucht anhand der Ähnlichkeit von Embedding-Vektoren.
- **BM25:** Bewertet Dokumente anhand ihrer Suchbegriffe.

Beide Verfahren liefern eine Rangliste relevanter Dokumente.

Das Problem: Ihre Bewertungen sind nicht direkt vergleichbar. BM25 liefert Ranking-Scores, während Chroma beispielsweise Vektordistanzen zurückgibt.

**Reciprocal Rank Fusion (RRF)** löst dieses Problem, indem es ausschließlich die Rangpositionen der Treffer berücksichtigt.

Die ursprünglichen Scores werden nicht benötigt.

## Wie funktioniert RRF?

Jeder Treffer erhält für seine Position in einem Ranking einen kleinen Punktwert.

Die Berechnung lautet:

```text
RRF-Beitrag = 1 / (k + Rangposition)
```

Dabei ist `k` eine Konstante, die bestimmt, wie stark sich die Rangpositionen auf die Bewertung auswirken.

Häufig wird `k = 60` verwendet.

Bei diesem Wert ergeben sich beispielsweise folgende Beiträge:

| Rangposition | RRF-Beitrag |
|---|---:|
| 1 | 0,016393 |
| 2 | 0,016129 |
| 3 | 0,015873 |

Ein Treffer auf Rang 1 erhält also etwas mehr Punkte als ein Treffer auf Rang 2.

**Kommt ein Dokument in mehreren Rankings vor, werden seine Beiträge addiert.**

Dadurch können Dokumente profitieren, die von mehreren Suchverfahren als relevant eingestuft werden.

## Was machen wir?

Wir verwenden zwei künstliche Rankings:

```text
BM25                 Dense Retrieval
----                 ---------------
1. A                 1. B
2. B                 2. C
3. C                 3. A
```

Unsere Aufgabe besteht darin, die Rangpositionen auszuwerten, die RRF-Beiträge zu addieren und daraus eine gemeinsame Rangliste zu erstellen.

Wir verwenden bewusst keine echte Datenbank und keine API.

So können wir uns vollständig auf den RRF-Algorithmus konzentrieren.

## Was zeigt der Output?

Nach der Berechnung erhalten wir:

| Rang | Chunk | RRF-Score |
|---|---|---:|
| 1 | **B** | **0,032522** |
| 2 | A | 0,032266 |
| 3 | C | 0,032002 |

Warum gewinnt Chunk B?

Er steht im BM25-Ranking auf Platz 2 und im Dense-Ranking auf Platz 1.

Sein Gesamtscore entsteht durch Addition der beiden Beiträge:

```text
B: 1/62 + 1/61 = 0,032522
```

Chunk A steht auf Platz 1 und Platz 3:

```text
A: 1/61 + 1/63 = 0,032266
```

Chunk C steht auf Platz 3 und Platz 2:

```text
C: 1/63 + 1/62 = 0,032002
```

**B gewinnt, weil es in beiden Rankings besonders weit oben steht.**

Der abschließende Test überprüft, ob die berechnete Reihenfolge `B, A, C` lautet.

## Warum ist das für RAG wichtig?

RRF ermöglicht es, unterschiedliche Retrieval-Verfahren zu kombinieren, ohne ihre Scores auf eine gemeinsame Skala umrechnen zu müssen.

Das ist besonders praktisch für **Hybrid Search**, bei der wir BM25 und Dense Retrieval gemeinsam einsetzen.

RRF hat allerdings auch Grenzen:

- Die ursprünglichen Relevanzwerte gehen verloren.
- Die Qualität hängt von den zugrunde liegenden Rankings ab.
- Ein hoher RRF-Score garantiert nicht, dass ein Dokument die Frage korrekt beantwortet.

In Station 08 wenden wir RRF auf echte Suchergebnisse aus unserem Teralune-Korpus an.

## Eigenes Experiment

Verändere die Reihenfolge der Chunks in den beiden Rankings.

Probiere außerdem einen anderen Wert für `RRF_K` aus, beispielsweise `10` oder `100`.

Beobachte, wie sich die RRF-Scores und gegebenenfalls die Rangfolge verändern.

## Merksatz

**RRF kombiniert mehrere Suchrankings anhand ihrer Rangpositionen. Dokumente, die in mehreren Rankings weit oben stehen, erhalten einen höheren Gesamtscore.**
