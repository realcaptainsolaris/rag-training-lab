# Station 09: Retrieval-Evaluation mit Goldfragen

## Lernziel

Du lernst, wie wir die Qualität unserer Dokumentensuche systematisch überprüfen.

Dafür verwenden wir einen kleinen Evaluationsdatensatz mit bekannten Fragen und erwarteten Suchergebnissen.

## Hintergrund

Bisher haben wir unsere Suchverfahren hauptsächlich durch Ausprobieren bewertet.

Wir haben Fragen gestellt, die gefundenen Chunks betrachtet und eingeschätzt, ob die Ergebnisse sinnvoll erscheinen.

Für eine systematische Bewertung reicht das nicht aus.

Wir benötigen:

1. **Testfragen**, die unser RAG-System beantworten können soll.
2. **Referenzinformationen**, die wir unabhängig von der Suche festlegen.
3. **Metriken**, mit denen wir die Suchergebnisse bewerten.

Einen solchen Evaluationsdatensatz nennen wir häufig **Goldset**.

Eine Testfrage mit ihrer erwarteten Referenzinformation bezeichnen wir als **Goldfrage**.

## Was machen wir?

Wir verwenden drei Goldfragen aus unserem Teralune-Korpus.

Für jede Frage haben wir vorher einen Chunk festgelegt, der die benötigte Information enthält.

| Goldfrage | Erwarteter Chunk |
|---|---|
| How long does a cursor remain valid? | D022_2 |
| How long is an Orbit 3 access token valid? | D002_1 |
| What is the next_cursor field used for? | D022_1 |

Anschließend führen wir für jede Frage eine semantische Suche durch.

Wir vergleichen die gefundenen Chunk-IDs mit der jeweils erwarteten ID.

**Wichtig:** Wir evaluieren ausschließlich das Retrieval. Eine LLM-Antwort wird in dieser Station nicht generiert.

## Was bedeutet Hit@k?

Hit@k ist eine einfache Metrik zur Bewertung von Suchergebnissen.

Sie beantwortet die Frage:

**Befindet sich der erwartete Chunk unter den ersten k Suchergebnissen?**

Bei Hit@3 betrachten wir die ersten drei Treffer.

```text
Gold-Chunk: D022_2

Gefundene Chunks:
1. D022_1
2. D022_2
3. D005_1

Ergebnis: Hit@3 = 1
```

Der erwartete Chunk wurde gefunden. Die Frage zählt deshalb als erfolgreich.

Wäre `D022_2` nicht unter den ersten drei Treffern, wäre Hit@3 gleich 0.

Für mehrere Goldfragen berechnen wir anschließend den Anteil erfolgreicher Fragen.

Beispiel:

```text
Goldfragen insgesamt:  10
Erfolgreiche Fragen:    8

Hit@3 = 8 / 10 = 80 %
```

Hit@k berücksichtigt nicht die genaue Position innerhalb der ersten k Treffer.

Ein Treffer auf Rang 1 zählt genauso wie ein Treffer auf Rang 3.

## Was zeigt der Output?

Unsere Evaluation liefert folgende Ergebnisse:

| Frage | Gold-Chunk | Gefundene Position | Hit@3 |
|---|---|---:|---:|
| Cursor-Gültigkeit | D022_2 | 1 | 1 |
| Orbit-3-Access-Token | D002_1 | 3 | 1 |
| Verwendung von next_cursor | D022_1 | 1 | 1 |

Das Gesamtergebnis lautet:

```text
RETRIEVAL-EVALUATION

Goldfragen: 3
Erfolgreich: 3
Hit@3: 100.0%
```

Alle drei erwarteten Chunks wurden gefunden.

**Ist unser Retriever damit perfekt?**

Nein.

Betrachten wir die zweite Frage genauer:

```text
Frage:
How long is an Orbit 3 access token valid?

Gefunden:
1. D004_2
2. D033_1
3. D002_1
```

Der erwartete Chunk `D002_1` steht erst auf Rang 3.

Auf Rang 1 befindet sich dagegen `D004_2`, ein historischer Chunk aus Orbit 2.4.

Dieser enthält die veraltete Token-Gültigkeit von **120 Minuten**.

Für Orbit 3.0 beträgt die Gültigkeit jedoch **60 Minuten**.

Unsere Evaluation bewertet diese Frage trotzdem als erfolgreich.

Das ist kein Berechnungsfehler, sondern eine Einschränkung der Metrik.

## Warum ist das für RAG wichtig?

Hit@k beantwortet eine wichtige, aber begrenzte Frage:

**Hat der Retriever die erwartete Information gefunden?**

Die Metrik sagt dagegen nicht aus:

- Ob die richtige Information auf Rang 1 steht.
- Ob zusätzlich veraltete oder irrelevante Chunks gefunden wurden.
- Ob das LLM die richtige Quelle verwendet.
- Ob die generierte Antwort fachlich korrekt ist.

Außerdem verwenden wir nur drei Goldfragen mit jeweils einem erwarteten Chunk. Für eine belastbare Evaluation ist das zu wenig.

In produktiven RAG-Systemen kombinieren wir deshalb mehrere Maßnahmen:

**Metadatenfilter** schränken die Suche auf zulässige Dokumente ein.

**Retrieval-Metriken** bewerten, welche Informationen gefunden werden.

**Grounding** soll sicherstellen, dass generierte Antworten auf den bereitgestellten Quellen beruhen.

Eine Garantie für korrekte Antworten ergibt sich daraus allerdings nicht.

## Eigenes Experiment

Verändere `TOP_K` und führe die Evaluation erneut aus.

Teste nacheinander:

```python
TOP_K = 1
TOP_K = 2
TOP_K = 3
```

Vergleiche die Ergebnisse.

Überlege anschließend:

**Warum kann Hit@3 einen Wert von 100 % erreichen, obwohl Hit@1 schlechter ausfällt?**

Und eine weiterführende Frage:

**Welche zusätzlichen Prüfungen wären notwendig, um die Qualität eines vollständigen RAG-Systems zu bewerten?**

## Merksatz

**Hit@k misst, ob ein erwarteter Chunk unter den ersten k Suchergebnissen vorkommt. Ein erfolgreiches Retrieval ist eine wichtige Voraussetzung für gute RAG-Antworten, garantiert aber weder die Verwendung der richtigen Quelle noch eine korrekte Antwort.**
