# Station 10: Grounding und Quellenbezug

## Lernziel

Du lernst, wie wir gefundene Dokumente als Kontext an ein LLM übergeben und Antworten anhand dieser Informationen generieren.

Außerdem untersuchen wir, wie das Modell reagiert, wenn der Kontext keine ausreichenden Informationen enthält.

## Hintergrund

Bisher haben wir hauptsächlich das **Retrieval** untersucht: Welche Dokumente findet unser RAG-System?

Jetzt ergänzen wir die Antwortgenerierung.

Dabei entsteht eine wichtige Herausforderung: Ein LLM besitzt bereits Wissen aus seinem Training. Es kann deshalb Antworten formulieren, die nicht aus unseren gefundenen Dokumenten stammen.

**Grounding** bedeutet, dass die generierte Antwort durch bereitgestellte Informationen gestützt sein soll.

Unser Ziel ist, dass das Modell nur Aussagen trifft, die sich anhand der gefundenen Quellen belegen lassen.

## Was machen wir?

Unsere RAG-Pipeline besteht jetzt aus folgenden Schritten:

```text
                 Benutzerfrage
                       |
                       v
                Dense Retrieval
                       |
                       v
               Metadatenfilter
              Version 3.0/current
                       |
                       v
                Top 3 Chunks
                       |
                       v
                Kontext aufbauen
                       |
                       v
                 LLM + Prompt
                       |
                       v
              Antwort mit Quellen
```

### 1. Dokumente suchen

Wir verwenden die Chroma-Collection aus Station 05.

Die Suche berücksichtigt ausschließlich Chunks mit folgenden Metadaten:

```text
version = "3.0"
status  = "current"
```

Damit verhindern wir, dass historische Dokumente aus Orbit 2.4 in den Kontext gelangen.

### 2. Kontext aufbauen

Die gefundenen Chunks werden zu einem gemeinsamen Text verbunden.

Jeder Abschnitt enthält seine Chunk-ID, die Quelldatei und den eigentlichen Dokumenttext.

Beispiel:

```text
Chunk-ID: D003_1
Quelle: D003.md

## Acceptance and deadline

Orbit 3.0 retries eligible failed webhook
deliveries for 72 hours from the first attempt.
```

Die Chunk-ID ermöglicht es dem LLM, seine Aussagen mit Quellenangaben zu versehen.

### 3. Antwort generieren

Wir verwenden die OpenAI Responses API mit dem Modell `gpt-4.1-mini`.

Das Modell erhält:

1. **Instructions:** Regeln für die Antwortgenerierung.
2. **Kontext:** Die gefundenen Dokumentabschnitte.
3. **Frage:** Die ursprüngliche Benutzerfrage.

Unsere Instructions verlangen unter anderem, ausschließlich den Kontext zu verwenden, keine Informationen zu erfinden und Quellen anzugeben.

## Was zeigt der Output?

Wir testen zwei unterschiedliche Situationen.

### Frage 1: Eine beantwortbare Frage

> Wie lange versucht Orbit 3.0 fehlgeschlagene Webhooks erneut?

Der Retriever findet unter anderem den Chunk `D003_1`.

Darin steht, dass Orbit 3.0 fehlgeschlagene Webhook-Zustellungen unter bestimmten Bedingungen **72 Stunden lang** erneut versucht.

Das Modell antwortet entsprechend und nennt die Quelle:

```text
Orbit 3.0 versucht fehlgeschlagene
Webhook-Zustellungen 72 Stunden lang erneut,
beginnend mit dem ersten Versuch.

[D003_1]
```

Die Antwort stimmt mit der gefundenen Dokumentation überein.

### Frage 2: Eine nicht beantwortbare Frage

> Welche offiziellen Rabatte bekommen Universitäten?

Unser Korpus enthält keine Informationen zu Universitätsrabatten.

Trotzdem liefert die Vektorsuche drei Chunks zurück.

Diese behandeln unter anderem API-Limits, Aufbewahrungsfristen und Webhook-Deduplizierung.

**Warum?**

Eine Vektorsuche sucht nach den ähnlichsten Dokumenten. Sie garantiert nicht, dass diese Dokumente die Frage beantworten können.

Das Modell erkennt in unserem Experiment, dass die benötigten Informationen fehlen.

Es antwortet:

> Die bereitgestellten Kontexte enthalten keine Informationen über offizielle Rabatte für Universitäten. Daher kann die Frage nicht beantwortet werden.

Dieses Verhalten nennt man **Abstention**: Das System verzichtet auf eine inhaltliche Antwort, wenn keine ausreichende Evidenz vorhanden ist.

## Warum ist das für RAG wichtig?

Grounding soll verhindern, dass ein LLM unbelegte Aussagen als Fakten präsentiert.

Allerdings gibt es wichtige Einschränkungen:

**Ein Grounding-Prompt ist keine technische Garantie.**

Das Modell kann weiterhin Informationen aus seinem Trainingswissen verwenden, Dokumente falsch interpretieren oder unbelegte Schlussfolgerungen ziehen.

Auch Quellenangaben sind kein Beweis für Faktentreue.

Ein Modell kann eine gültige Chunk-ID nennen, obwohl die zugehörige Quelle seine Aussage nicht tatsächlich unterstützt.

Deshalb müssen wir unterscheiden zwischen:

| Eigenschaft | Bedeutung |
|---|---|
| Retrieval-Relevanz | Wurden passende Dokumente gefunden? |
| Grounding | Ist die Antwort durch den Kontext gestützt? |
| Quellenbezug | Lassen sich Aussagen konkreten Quellen zuordnen? |
| Faktische Korrektheit | Sind die Aussagen tatsächlich richtig? |

Diese Eigenschaften hängen zusammen, sind aber nicht identisch.

## Eigenes Experiment

Verändere die Fragen in `QUESTIONS`.

Teste beispielsweise eine Frage, die nur teilweise durch den Korpus beantwortet werden kann.

Beobachte, ob das Modell fehlende Informationen erkennt oder versucht, eine vollständige Antwort zu formulieren.

Untersuche außerdem, ob die angegebenen Chunk-IDs tatsächlich die jeweiligen Aussagen belegen.

## Merksatz

**Grounding soll LLM-Antworten an überprüfbare Quellen binden. Ein guter Grounding-Prompt reduziert das Risiko unbelegter Aussagen, garantiert aber keine Faktentreue.**
