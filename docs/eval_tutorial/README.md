# RAG-Evaluation mit Python

In den bisherigen Übungen haben wir Dokumente in Chunks zerlegt, Embeddings erzeugt und relevante Informationen mit Chroma gesucht. Anschließend konnte ein Sprachmodell diese Informationen verwenden, um Fragen zu beantworten.

Aber woher wissen wir, ob unser RAG-System tatsächlich gut funktioniert?

Eine plausible Antwort ist nicht automatisch eine korrekte Antwort. Und selbst wenn die Antwort richtig ist, bedeutet das nicht, dass unser Retriever die passenden Informationen gefunden hat.

In diesem Tutorial lernen wir deshalb zwei unterschiedliche Formen der RAG-Evaluation kennen:

1. **Retrieval-Evaluation:** Findet unser System die relevanten Chunks?
2. **Answer-Evaluation:** Ist die generierte Antwort korrekt und durch den gefundenen Kontext belegt?

## 1. Das Goldset

Um die Qualität eines RAG-Systems zu messen, benötigen wir einen Referenzdatensatz, das sogenannte **Goldset**.

Unser Goldset befindet sich in `goldset.json` und enthält fünf Testfälle aus dem fiktiven Teralune-Korpus.

Jeder Testfall besteht aus drei wesentlichen Bestandteilen:

| Bestandteil | Bedeutung |
|---|---|
| Goldfrage | Eine Testfrage mit bekannter erwarteter Antwort |
| Gold-Antwort | Die erwartete Antwort auf diese Frage |
| Gold-Chunks | Die als relevant gekennzeichneten Textabschnitte |

Beispiel:

**Goldfrage:**

> How long is an Orbit 3.0 access token valid?

**Gold-Antwort:**

> 60 minutes

**Gold-Chunks:**

- `D002_1`
- `D033_1`
- `D005_1`

Alle drei Chunks enthalten Informationen, die die erwartete Antwort stützen.

Die Gold-Chunks bilden unsere Referenz für die Retrieval-Evaluation. Die Goldfrage und die Gold-Antwort bilden gemeinsam die Referenz für die Correctness-Bewertung.

Ein Goldset wird normalerweise sorgfältig zusammengestellt und fachlich überprüft. Fehlerhafte oder unvollständige Referenzdaten können zu irreführenden Evaluationsergebnissen führen.

## 2. Retrieval-Evaluation

Bei der Retrieval-Evaluation untersuchen wir, welche Chunks unser Retriever zurückliefert.

Dazu vergleichen wir die gefundenen Chunk-IDs mit den Gold-Chunks.

In unserem Tutorial betrachten wir jeweils die ersten drei Treffer (`k = 3`).

### Hit@k

**Hit@k** beantwortet die Frage:

*Ist mindestens ein relevanter Chunk unter den ersten k Treffern?*

Sobald mindestens ein Gold-Chunk gefunden wurde, beträgt Hit@k den Wert 1. Andernfalls beträgt er 0.

### Precision@k

**Precision@k** beantwortet die Frage:

*Welcher Anteil der ersten k Treffer ist relevant?*

Beispiel: Unter drei gefundenen Chunks sind zwei relevant.

Precision@3 = 2 / 3 = 0,667

### Recall@k

**Recall@k** beantwortet die Frage:

*Welcher Anteil aller bekannten Gold-Chunks wurde gefunden?*

Beispiel: Insgesamt existieren acht Gold-Chunks. Unter den ersten fünf Suchergebnissen befinden sich drei davon.

Recall@5 = 3 / 8 = 0,375

Der Retriever hat damit **37,5 % aller relevanten Gold-Chunks** gefunden.

### MRR@k

**Mean Reciprocal Rank (MRR@k)** berücksichtigt, an welcher Position der erste relevante Treffer erscheint.

Für jede Frage berechnen wir zunächst den Reciprocal Rank (RR):

RR = 1 / Rang des ersten relevanten Treffers

Steht der erste relevante Chunk auf Rang 2, beträgt RR = 0,5.

Wird innerhalb der ersten k Treffer kein relevanter Chunk gefunden, beträgt RR = 0.

MRR@k ist der Mittelwert dieser Werte über alle Testfragen.

### Warum mehrere Metriken?

Ein Retriever kann bei jeder Frage mindestens einen relevanten Chunk finden und trotzdem viele irrelevante Treffer zurückliefern.

Ebenso kann ein relevanter Chunk erst an dritter Stelle erscheinen.

Deshalb betrachten wir mehrere Metriken gemeinsam.

In unserem Tutorial erhalten wir nach Implementierung der Metriken folgende Ergebnisse:

| Metrik | Ergebnis |
|---|---:|
| Mean Hit@3 | 1,000 |
| Mean Precision@3 | 0,467 |
| Mean Recall@3 | 0,800 |
| MRR@3 | 0,400 |

Obwohl bei jeder Frage mindestens ein relevanter Chunk gefunden wird, sind weniger als die Hälfte der zurückgegebenen Chunks relevant.

**Wichtig:** Diese Ergebnisse stammen aus bewusst simulierten Rankings. Wir messen hier keine echte Chroma-Suche, sondern lernen zunächst die Berechnung und Interpretation der Metriken.

## 3. Answer-Evaluation

Beim Retrieval bewerten wir die gefundenen Informationen. Bei der Answer-Evaluation bewerten wir dagegen die Antwort des Sprachmodells.

Wir unterscheiden zwei Dimensionen.

### Correctness

**Correctness:** Stimmt die generierte Antwort mit der Goldfrage und der erwarteten Gold-Antwort überein?

Die Gold-Antwort ist unsere Referenz. Der tatsächlich abgerufene Kontext wird für diese Bewertung nicht verwendet.

### Faithfulness

**Faithfulness:** Werden die Aussagen der generierten Antwort durch den Retrieval-Kontext gestützt?

Hier betrachten wir ausschließlich die Informationen, die dem Sprachmodell als Kontext bereitgestellt wurden.

Die Gold-Antwort wird bewusst nicht zur Bewertung herangezogen.

### Beispiel

Unser Sprachmodell liefert folgende Antwort:

> An Orbit 3.0 access token is valid for 60 minutes. The platform automatically renews every token after 30 minutes.

Die erste Behauptung stimmt mit unserer Gold-Antwort überein.

Die zweite Behauptung über die automatische Erneuerung ist dagegen nicht durch die Gold-Antwort belegt.

Außerdem enthält der simulierte Retrieval-Kontext lediglich Informationen über Orbit 2.4, nicht über die konkrete Token-Gültigkeit von Orbit 3.0.

Damit entsteht eine interessante Situation:

**Eine Aussage kann mit der Gold-Antwort übereinstimmen, ohne durch den abgerufenen Kontext belegt zu sein.**

## 4. LLM-as-a-Judge

Für die Answer-Evaluation verwenden wir ein Sprachmodell als Bewertungsinstanz.

Dieses Verfahren wird als **LLM-as-a-Judge** bezeichnet.

Der Judge zerlegt die generierte Antwort in einzelne Behauptungen und bewertet jede Behauptung anhand einer vorgegebenen Referenz.

Dabei verwendet er drei Kategorien:

| Kategorie | Bedeutung |
|---|---|
| SUPPORTED | Die Referenz stützt die Behauptung |
| CONTRADICTED | Die Referenz widerspricht der Behauptung |
| UNKNOWN | Die Referenz bestätigt oder widerlegt die Behauptung nicht |

`UNKNOWN` bedeutet ausdrücklich nicht, dass eine Behauptung falsch ist. Es bedeutet lediglich, dass die vorhandene Referenz keine ausreichende Bewertung ermöglicht.

LLM-Judges sind nicht unfehlbar. Ihre Ergebnisse können vom verwendeten Modell, vom Prompt und von der Formulierung der Referenzinformationen abhängen.

## 5. Die beiden Übungen

### Übung 1: Retrieval-Evaluation

Datei: `retrieval_eval.py`

Wir verwenden fünf Goldfragen und simulierte Retrieval-Rankings.

Wir berechnen Hit@3, Precision@3, Recall@3 und MRR@3 und interpretieren die Ergebnisse.

Anleitung: [Retrieval-Evaluation](retrieval_eval.md)

Start:

```bash
uv run python -m eval_tutorial.retrieval_eval
```

Diese Übung benötigt weder eine OpenAI-API noch eine Chroma-Datenbank.

### Übung 2: Answer-Evaluation

Datei: `answer_eval.py`

Wir bewerten eine simulierte RAG-Antwort anhand zweier unterschiedlicher Referenzen.

Dazu verwenden wir zwei LLM-Judges:

1. Einen Correctness-Judge mit Goldfrage und Gold-Antwort.
2. Einen Faithfulness-Judge mit dem simulierten Retrieval-Kontext.

Anleitung: [Answer-Evaluation](answer_eval.md)

Start:

```bash
uv run python -m eval_tutorial.answer_eval
```

Diese Übung benötigt einen gültigen OpenAI-API-Key.

## 6. Was wir aus der Evaluation lernen

Retrieval-Evaluation und Answer-Evaluation untersuchen unterschiedliche Fehlerquellen.

Ein RAG-System kann relevante Informationen finden und trotzdem eine falsche Antwort erzeugen.

Umgekehrt kann ein Sprachmodell eine korrekte Aussage formulieren, obwohl diese nicht durch den gefundenen Kontext gestützt wird.

**Die zentrale Erkenntnis:**

Ein gutes RAG-System muss sowohl relevante Informationen finden als auch Antworten erzeugen, die korrekt und durch diese Informationen belegt sind.

Deshalb sollten wir Retrieval und Antwortgenerierung getrennt evaluieren.
