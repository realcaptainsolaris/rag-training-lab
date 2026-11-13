# Station 06: Lexikalische Suche mit BM25

## Lernziel

Du lernst BM25 als Alternative zur semantischen Vektorsuche kennen und verstehst, warum die Suche nach konkreten Begriffen manchmal besser funktioniert als die Suche mit Embeddings.

## Hintergrund

Bisher haben wir **Dense Retrieval** verwendet: Dokumente und Suchfragen werden in Embedding-Vektoren umgewandelt und anhand ihrer Ähnlichkeit verglichen.

**BM25 (Best Matching 25)** verfolgt einen anderen Ansatz.

BM25 ist ein lexikalisches Rankingverfahren. Es bewertet Dokumente anhand der Suchbegriffe, die darin vorkommen.

Dabei berücksichtigt es insbesondere:

1. **Term Frequency (TF):** Wie häufig kommt ein Suchbegriff im Dokument vor?
2. **Inverse Document Frequency (IDF):** Wie selten ist der Begriff im gesamten Dokumentbestand?
3. **Dokumentlänge:** Wie lang ist das Dokument im Verhältnis zu den anderen Dokumenten?

Seltene, charakteristische Begriffe können dadurch stärker gewichtet werden als häufig vorkommende Wörter.

BM25 benötigt keine Embeddings und kein Sprachmodell. Das Verfahren wird bereits seit den 1990er-Jahren in der klassischen Information Retrieval-Forschung eingesetzt und gehört bis heute zu den etablierten Rankingverfahren für Volltextsuchen. Suchmaschinen und Suchplattformen wie Elasticsearch, Apache Lucene und OpenSearch verwenden BM25 als Standardverfahren zur Bewertung der Relevanz von Texttreffern. BM25 ist also keine neue Entwicklung aus dem Umfeld generativer KI, sondern ein seit Jahrzehnten bewährtes Verfahren, das auch in modernen RAG-Systemen eine wichtige Rolle spielt.



## Was machen wir?

### 1. Dokumente laden

Wir verwenden die 42 Chunks aus Station 05.

Chroma dient diesmal ausschließlich als Dokumentenspeicher. Die vorhandenen Embeddings werden nicht benötigt.

### 2. Texte tokenisieren

Für BM25 zerlegen wir die Texte in Suchbegriffe.

Unsere einfache Tokenisierung verwendet einen regulären Ausdruck und wandelt alle Wörter in Kleinbuchstaben um.

Beispiel:

```text
"Error AUTH-104!"
```

wird zu:

```python
["error", "auth", "104"]
```

**Wichtig:** Diese Tokenisierung unterscheidet sich von der Modell-Tokenisierung aus Station 00.

Wir erzeugen hier keine Token-IDs für ein Sprachmodell, sondern Wörter und Zeichenfolgen für die lexikalische Suche.

### 3. BM25-Index erstellen

Mit der Bibliothek `rank-bm25` bauen wir einen BM25-Index im Arbeitsspeicher auf.

Anschließend berechnen wir für jede Suchfrage einen Score pro Chunk.

Die Ergebnisse werden absteigend nach Score sortiert.

## Was zeigt der Output?

### Frage 1: Wie lange ist ein Cursor gültig?

```text
How long does a cursor remain valid?
```

Die Suche liefert unter anderem:

| Rang | Chunk | BM25-Score |
|---|---|---:|
| 1 | D022_2 | **5,658** |
| 2 | D022_5 | 5,288 |
| 3 | D005_1 | 4,807 |
| 4 | D022_1 | 4,732 |
| 5 | D022_3 | 4,444 |

Der erste Treffer enthält die gesuchte Information:

> A cursor expires after 15 minutes.

BM25 findet damit einen relevanten Abschnitt über die Gültigkeit von Cursorn.

### Frage 2: Suche nach einem technischen Bezeichner

```text
next_cursor
```

Der beste Treffer lautet:

| Rang | Chunk | BM25-Score |
|---|---|---:|
| 1 | D022_1 | **3,141** |

Der Chunk enthält den Bezeichner `next_cursor` und beschreibt seine Verwendung bei der Pagination.

Das zeigt eine Stärke lexikalischer Suche: **Exakte technische Begriffe können gezielt gefunden werden.**

## BM25 und Dense Retrieval im Vergleich

| Eigenschaft | BM25 | Dense Retrieval |
|---|---|---|
| Grundlage | Suchbegriffe | Embeddings |
| Semantische Ähnlichkeit | Nicht direkt | Ja |
| Exakte Bezeichner | Häufig sehr gut | Nicht immer zuverlässig |
| Synonyme erkennen | Eingeschränkt | Häufig gut |
| Embedding-Modell erforderlich | Nein | Ja |

BM25 ist besonders interessant für Fehlercodes, Produktnummern, API-Bezeichner und andere charakteristische Zeichenfolgen.

Dense Retrieval kann dagegen auch dann passende Dokumente finden, wenn die Suchfrage andere Wörter verwendet als der Dokumenttext.

## Warum ist das für RAG wichtig?

Beide Suchverfahren besitzen unterschiedliche Stärken.

In vielen RAG-Systemen ist es deshalb sinnvoll, **lexikalische und semantische Suche zu kombinieren**.

Diesen Ansatz nennen wir *Hybrid Search*.

In den nächsten Stationen lernen wir, wie sich die Ergebnisse beider Suchverfahren zusammenführen lassen.

## Eigenes Experiment

Verändere die Suchfragen und verwende beispielsweise einen API-Bezeichner, einen Fehlercode oder eine natürlich formulierte Frage.

Beobachte, welche Begriffe BM25 besonders stark gewichtet und welche Chunks dadurch auf den ersten Plätzen erscheinen.

## Merksatz

**BM25 bewertet die Übereinstimmung von Suchbegriffen. Dense Retrieval bewertet semantische Ähnlichkeit. Beide Verfahren ergänzen sich und können gemeinsam bessere Suchergebnisse liefern.**
