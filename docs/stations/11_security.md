# Station 11: Zugriffskontrolle (ACL) bei RAG

## Lernziel

Du lernst, wie wir eine Vektorsuche anhand von Benutzerrechten absichern.

Dabei verwenden wir Metadatenfilter, um sicherzustellen, dass Benutzer ausschließlich Dokumente finden, für die sie eine Leseberechtigung besitzen.

## Hintergrund

In einem Unternehmen enthält eine Wissensdatenbank häufig Informationen mit unterschiedlichen Zugriffsrechten.

Beispielsweise:

- Öffentliche Produktdokumentation
- Kundenspezifische Supportfälle
- Vertrauliche Sicherheitsinformationen

Ein RAG-System darf diese Informationen nicht beliebig an alle Benutzer weitergeben.

Das gilt bereits für das Retrieval.

**Ein Dokument, das ein Benutzer nicht lesen darf, darf auch nicht als Kontext an das LLM übergeben werden.**

Die dafür verwendeten Zugriffsregeln nennen wir **Access Control Lists (ACL)**.

## Was machen wir?

Für diese Station erstellen wir einen eigenen Chroma-Index mit drei Dokumenten.

| Dokument | Zugriffsklasse | Berechtigung |
|---|---|---|
| D003 | PUBLIC | Alle Benutzer |
| D008 | CUSTOMER | Kunden der Organisation `org-amber` |
| D010 | RESTRICTED | Benutzer mit Rolle `security_admin` |

Wir simulieren drei Benutzer:

| Benutzer | PUBLIC | CUSTOMER (org-amber) | RESTRICTED |
|---|---|---|---|
| anonymous | Ja | Nein | Nein |
| customer_basic | Ja | Ja | Nein |
| security_admin | Ja | Nein | Ja |

Bemerkenswert ist die letzte Zeile: Der Security Admin erhält in unserem Beispiel **nicht automatisch Zugriff auf Kundendokumente**.

Berechtigungen ergeben sich aus konkreten Regeln, nicht aus einer allgemeinen Vorstellung von Benutzerhierarchien.

### 1. Dokumente indexieren

Wir speichern die drei Dokumente mit ihren Embeddings und Zugriffsmetadaten in Chroma.

Anders als in den vorherigen Stationen indexieren wir hier jedes Dokument als einen einzelnen Eintrag.

### 2. ACL-Filter erstellen

Die Funktion `build_acl_filter()` erstellt für jeden Benutzer einen passenden Metadatenfilter.

Ein anonymer Benutzer darf beispielsweise nur öffentliche Dokumente sehen:

```python id="u30b1s"
{"access": "PUBLIC"}
```

Für einen Kunden aus `org-amber` wird der Filter um die kundenspezifische Berechtigung erweitert.

### 3. Geschützte Suche ausführen

Die entscheidende Stelle ist der Parameter `where` in der Chroma-Abfrage.

```python id="l5x2jb"
results = collection.query(
    query_embeddings=[question_vector],
    n_results=top_k,
    where=acl_filter,
)
```

Damit beschränken wir die Suche auf Dokumente, die der Benutzer lesen darf.

Wir suchen also nicht zuerst im gesamten Bestand, um anschließend unerlaubte Treffer aus der Ergebnisliste zu entfernen.

## Was zeigt der Output?

Alle drei Benutzer stellen dieselben Fragen.

Nur ihre Zugriffsrechte unterscheiden sich.

Die Ergebnisse zeigen, ob das jeweils gesuchte Dokument gefunden wird:

| Gesuchtes Dokument | anonymous | customer_basic | security_admin |
|---|---|---|---|
| D003 (PUBLIC) | Gefunden | Gefunden | Gefunden |
| D008 (CUSTOMER) | Nicht gefunden | Gefunden | Nicht gefunden |
| D010 (RESTRICTED) | Nicht gefunden | Nicht gefunden | Gefunden |

Das entspricht genau unseren Berechtigungsregeln.

### Beispiel: Kundenspezifischer Supportfall

Die Frage lautet:

> Why did measurements stop after the key rotation in TRAIN-208?

Der anonyme Benutzer erhält ausschließlich `D003`.

Der Kunde aus `org-amber` erhält dagegen `D008` als besten Treffer.

Der Security Admin findet `D008` ebenfalls nicht.

**Die Suchfrage ist identisch. Der Unterschied entsteht ausschließlich durch die Zugriffsrechte.**

### Warum gibt es trotzdem Treffer?

Bei der Frage nach dem geschützten Sicherheitsmarker erhält der anonyme Benutzer `D003` als Suchergebnis.

Das bedeutet nicht, dass `D003` die Frage beantworten kann.

Chroma liefert den ähnlichsten Treffer **innerhalb der erlaubten Dokumente**.

Damit greifen zwei unterschiedliche Konzepte ineinander:

**Zugriffskontrolle:** Welche Dokumente darf der Benutzer überhaupt durchsuchen?

**Semantische Relevanz:** Welche der erlaubten Dokumente passen am besten zur Frage?

Ein erlaubter Treffer ist nicht automatisch ein relevanter Treffer.

## Warum ist das für RAG wichtig?

Ein Grounding-Prompt kann keine Zugriffskontrolle ersetzen.

Wenn vertrauliche Informationen bereits im LLM-Kontext stehen, ist es zu spät, sich ausschließlich auf die Anweisung zu verlassen, diese Informationen nicht preiszugeben.

Deshalb muss die Zugriffskontrolle vor der Antwortgenerierung greifen.

Für ein produktives System gelten außerdem weitere Anforderungen:

- Benutzer müssen zuverlässig authentifiziert werden.
- Berechtigungen müssen aus einer vertrauenswürdigen Quelle stammen.
- Der Benutzer darf den ACL-Filter nicht selbst bestimmen.
- Änderungen an Berechtigungen müssen bei nachfolgenden Suchanfragen berücksichtigt werden.

Unsere Station demonstriert das grundlegende Prinzip anhand einer kleinen, kontrollierten Umgebung.

## Eigenes Experiment

Untersuche die Funktion `build_acl_filter()`.

Verändere anschließend testweise die Organisation von `customer_basic` zu `org-blue`.

Was passiert mit dem Zugriff auf `D008`?

Überlege außerdem:

**Warum reicht es nicht aus, vertrauliche Dokumente erst nach der Vektorsuche aus der Ergebnisliste zu entfernen?**

## Merksatz

**Zugriffskontrolle gehört in den Retrieval-Prozess. Ein RAG-System darf nur Dokumente als Kontext verwenden, für die der jeweilige Benutzer eine Leseberechtigung besitzt.**
