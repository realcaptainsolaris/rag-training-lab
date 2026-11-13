# Answer-Evaluation: Correctness und Faithfulness

## Lernziel

Du lernst, wie wir die Qualität einer generierten RAG-Antwort bewerten.

Dabei unterscheiden wir zwei Eigenschaften:

1. **Correctness:** Stimmt die Antwort mit unserer Gold-Antwort überein?
2. **Faithfulness:** Werden die Aussagen durch den gefundenen Retrieval-Kontext gestützt?

Für die Bewertung verwenden wir ein Sprachmodell als **LLM-as-a-Judge**.

## Hintergrund

Bisher haben wir untersucht, ob unser Retriever relevante Dokumente findet und ob ein Sprachmodell daraus Antworten generieren kann.

Aber eine Antwort kann sachlich korrekt sein, ohne durch die gefundenen Dokumente belegt zu werden.

Umgekehrt kann eine Antwort vollständig auf dem Kontext beruhen, obwohl dieser veraltete oder falsche Informationen enthält.

Deshalb bewerten wir Correctness und Faithfulness getrennt.

## Was machen wir?

Wir verwenden einen vorbereiteten Testfall aus unserem Teralune-Goldset.

**Goldfrage:**

> How long is an Orbit 3.0 access token valid?

**Gold-Antwort:**

> 60 minutes

Unser simulierter Retriever hat allerdings einen historischen Chunk aus Orbit 2.4 gefunden:

```text
[D004_2] Webhook Delivery in Orbit 2.4

The access-token lifetime in Orbit 2.4 is 120 minutes.
A new client that assumes the same lifetime in Orbit 3.0
may continue using an expired token.
```

Die simulierte Antwort lautet:

> An Orbit 3.0 access token is valid for 60 minutes. The platform automatically renews every token after 30 minutes.

Die Antwort enthält zwei Behauptungen:

1. Ein Orbit-3.0-Token ist 60 Minuten gültig.
2. Die Plattform erneuert jedes Token automatisch nach 30 Minuten.

Wir lassen beide Behauptungen durch zwei unterschiedliche LLM-Judges bewerten.

### 1. Correctness bewerten

Der Correctness-Judge erhält die Goldfrage, die Gold-Antwort und die vom LLM generierte Antwort auf die Benutzerfrage. In unserem Experiment ist diese LLM-Antwort simuliert. Der Judge überprüft, ob ihre Aussagen mit der Goldfrage und der erwarteten Gold-Antwort übereinstimmen.


### 2. Faithfulness bewerten


Der Faithfulness-Judge erhält die ursprüngliche Benutzerfrage, die von der Vektordatenbank gefundenen Textabschnitte (Retrieval-Kontext) und die daraus vom LLM generierte Antwort. Er überprüft, ob die Aussagen des LLM durch diese Textabschnitte belegt sind. In unserem Experiment sind sowohl die gefundenen Textabschnitte als auch die LLM-Antwort simuliert.

Die Gold-Antwort wird bewusst nicht übergeben.


Beide Judges verwenden drei Bewertungskategorien:

| Kategorie | Bedeutung |
|---|---|
| SUPPORTED | Die Referenz stützt die Behauptung |
| CONTRADICTED | Die Referenz widerspricht der Behauptung |
| UNKNOWN | Die Referenz bestätigt oder widerlegt die Behauptung nicht |

## Was zeigt der Output?

Starte das Programm:

```bash
uv run python -m eval_tutorial.answer_eval
```

### Correctness

Der erste Judge liefert:

| Behauptung | Bewertung |
|---|---|
| Token ist 60 Minuten gültig | SUPPORTED |
| Automatische Erneuerung nach 30 Minuten | UNKNOWN |

**Gesamturteil: `NOT_EVALUABLE`**

Die erste Aussage stimmt mit unserer Gold-Antwort überein.

Für die zweite Aussage enthält die Gold-Antwort keine ausreichenden Informationen.

Der Judge kann deshalb nicht bestätigen, ob die gesamte Antwort korrekt ist.

### Faithfulness

Der zweite Judge liefert:

| Behauptung | Bewertung |
|---|---|
| Token ist 60 Minuten gültig | UNKNOWN |
| Automatische Erneuerung nach 30 Minuten | UNKNOWN |

**Gesamturteil: `NOT_FAITHFUL`**

Der Retrieval-Kontext enthält lediglich Informationen zur historischen Produktversion Orbit 2.4.

Die Angabe von 60 Minuten für Orbit 3.0 wird durch diesen Kontext nicht belegt.

Auch die automatische Token-Erneuerung wird nicht erwähnt.

Damit ist keine der beiden Aussagen ausreichend durch den Kontext gestützt.

## Warum ist das für RAG wichtig?

Unser Beispiel zeigt, dass Correctness und Faithfulness unterschiedliche Fragen beantworten.

| | Correctness | Faithfulness |
|---|---|---|
| Referenz | Goldfrage und Gold-Antwort | Retrieval-Kontext |
| Bewertet | Übereinstimmung mit der erwarteten Antwort | Belegbarkeit durch den Kontext |
| Ergebnis | NOT_EVALUABLE | NOT_FAITHFUL |

**Eine sachlich richtige Aussage kann nicht faithful sein, wenn der Retrieval-Kontext sie nicht belegt.**

Dabei müssen wir beachten, dass unser Correctness-Judge keine unabhängige Wahrheitsprüfung durchführt. Er bewertet die Übereinstimmung mit der vorgegebenen Gold-Antwort.

Außerdem sind LLM-Judge-Urteile nicht deterministisch garantiert. Sie können vom Modell und von den Bewertungsregeln abhängen.

## Eigenes Experiment

Verändere den simulierten `RETRIEVAL_CONTEXT`.

Verwende beispielsweise einen Chunk, der die Token-Gültigkeit für Orbit 3.0 korrekt mit 60 Minuten beschreibt.

Führe die Evaluation erneut aus.

Beobachte, wie sich die Faithfulness-Bewertung verändert.

Entferne anschließend die unbelegte Behauptung über die automatische Token-Erneuerung aus `GENERATED_ANSWER`.

Vergleiche die neuen Ergebnisse mit den ursprünglichen Bewertungen.

## Merksatz

**Correctness bewertet die Übereinstimmung mit der Gold-Antwort. Faithfulness bewertet, ob die generierte Antwort durch den Retrieval-Kontext belegt ist. Beide Eigenschaften müssen getrennt untersucht werden.**
