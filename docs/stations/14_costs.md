# Station 14: Tokenverbrauch und API-Kosten

## Lernziel

Du lernst, den tatsächlichen Tokenverbrauch einer RAG-Pipeline zu messen und daraus die API-Kosten zu berechnen.

Wir untersuchen außerdem, wie sich die Menge des Retrieval-Kontexts auf die Antwortqualität auswirkt.

## Hintergrund

Eine RAG-Anfrage kann mehrere kostenpflichtige API-Aufrufe enthalten.

In unserem Beispiel entstehen Kosten für zwei Verarbeitungsschritte:

1. **Embedding:** Die Benutzerfrage wird in einen Vektor umgewandelt.
2. **LLM:** Die Frage wird zusammen mit dem gefundenen Kontext verarbeitet und beantwortet.

Bei der LLM-Nutzung unterscheiden wir zwischen **Input-Tokens** und **Output-Tokens**.

Input-Tokens entstehen durch die Eingabe an das Modell, beispielsweise Instructions, Suchfrage und Retrieval-Kontext.

Output-Tokens entstehen bei der Antwortgenerierung.

Beide Tokenarten können unterschiedlich viel kosten.

## Was machen wir?

Wir stellen dreimal dieselbe Frage:

> How long is an Orbit 3 access token valid?

Dabei verändern wir ausschließlich die Anzahl der Chunks, die wir dem LLM übergeben.

| Experiment | Retrieval-Kontext |
|---|---|
| A | Top 1 Chunk |
| B | Top 3 Chunks |
| C | Top 10 Chunks |

Die Suchfrage wird nur einmal eingebettet.

Anschließend holen wir die zehn ähnlichsten Chunks aus Chroma.

Für jedes Experiment verwenden wir die ersten 1, 3 oder 10 Treffer dieser Liste.

Dadurch bleibt die ursprüngliche Reihenfolge identisch.

### Die Verarbeitung

```text id="ufh16c"
                   Suchfrage
                       |
                       v
                OpenAI Embedding
                       |
                       v
                 Chroma Top 10
                       |
           +-----------+-----------+
           |           |           |
           v           v           v
         Top 1       Top 3       Top 10
           |           |           |
           v           v           v
          LLM         LLM         LLM
           |           |           |
           v           v           v
       Antwort A   Antwort B   Antwort C
           |           |           |
           +-----------+-----------+
                       |
                       v
              Kosten vergleichen
```

## Wie berechnen wir die Kosten?

Die API liefert uns den tatsächlichen Tokenverbrauch.

Wir lesen die Werte aus den `usage`-Informationen der Antworten.

Die Kosten berechnen wir anhand des jeweiligen Preises pro einer Million Tokens.

Beispiel:

```text id="dxk3yb"
500.000 Tokens
Preis: 0,40 USD pro Million Tokens

Kosten = 500.000 / 1.000.000 × 0,40 USD
       = 0,20 USD
```

Für eine vollständige RAG-Anfrage addieren wir die Kosten für das Frage-Embedding, die LLM-Eingabe und die LLM-Ausgabe.

Die im Code verwendeten Preise sind **Beispielwerte** und keine verbindliche aktuelle Preisliste.

## Was zeigt der Output?

### 1. Embedding-Kosten

Für unsere Suchfrage meldet die API:

```text id="j3qlay"
Embedding-Tokens: 11
Embedding-Kosten: $0.00000022
```

Die Kosten für das Frage-Embedding sind in diesem Beispiel sehr gering.

### 2. LLM-Kosten

Die drei Experimente liefern folgende Messwerte:

| Top K | Input-Tokens | Output-Tokens | Kosten pro Anfrage |
|---|---:|---:|---:|
| 1 | 174 | 17 | $0.000097 |
| 3 | 439 | 16 | $0.000201 |
| 10 | 1.053 | 16 | $0.000447 |

Mit mehr Chunks steigt der Input-Tokenverbrauch deutlich.

Die Anzahl der Output-Tokens bleibt dagegen nahezu unverändert.

Das liegt daran, dass die Frage eine kurze Antwort erfordert.

### 3. Verändert sich die Antwort?

**Top 1:**

Chroma liefert ausschließlich `D004_2`, einen historischen Chunk zu Orbit 2.4.

Das LLM antwortet:

> The context does not specify the access token lifetime for Orbit 3.0.

Das Modell erkennt, dass der bereitgestellte Kontext die Frage nicht ausreichend beantwortet.

**Top 3:**

Jetzt enthält der Kontext zusätzlich die Chunks `D033_1` und `D002_1`.

Beide enthalten die korrekte Information.

Das LLM antwortet:

> An Orbit 3.0 access token is valid for 60 minutes.

**Top 10:**

Die Antwort bleibt unverändert.

Obwohl wir wesentlich mehr Kontext übergeben, erhalten wir keine zusätzliche Information, die für diese Frage notwendig wäre.

## Was bedeutet das für die monatlichen Kosten?

Wir rechnen mit 10.000 Anfragen pro Monat.

| Top K | Monatliche API-Kosten |
|---|---:|
| 1 | $0.97 |
| 3 | $2.01 |
| 10 | $4.47 |

Die Unterschiede erscheinen zunächst gering.

Allerdings betrachten wir nur eine kurze Frage, einen kleinen Dokumentbestand und ein vergleichsweise günstiges Sprachmodell.

Bei größeren Kontexten, teureren Modellen oder sehr hohen Anfragezahlen können die Unterschiede erheblich werden.

Außerdem enthält unsere Berechnung nicht sämtliche Betriebskosten.

Beispielsweise fehlen die Kosten für die ursprüngliche Dokumentindexierung, den Betrieb der Vektordatenbank und mögliche zusätzliche Modellaufrufe.

## Warum ist das für RAG wichtig?

Unser Experiment zeigt einen wichtigen Zusammenhang:

**Mehr Kontext bedeutet nicht automatisch bessere Antworten.**

Bei Top 1 fehlt die benötigte Information.

Bei Top 3 ist sie vorhanden und das LLM beantwortet die Frage korrekt.

Top 10 liefert dieselbe Antwort, verursacht aber deutlich höhere Kosten.

Das bedeutet nicht, dass Top 3 grundsätzlich optimal ist.

Bei anderen Fragen könnten mehr Dokumente notwendig sein.

Wir müssen deshalb einen sinnvollen Kompromiss zwischen Retrieval-Qualität, Kontextgröße, Antwortqualität und Kosten finden.

Genau dafür benötigen wir die Evaluation aus Station 09.

## Eigenes Experiment

Verändere `TOP_K_VALUES` und beobachte die Auswirkungen auf den Tokenverbrauch.

Teste außerdem eine andere Suchfrage.

Vergleiche, ob mehr Kontext tatsächlich zusätzliche Informationen liefert oder nur die Kosten erhöht.

Überlege:

**Wäre es sinnvoller, zehn Chunks an das LLM zu übergeben oder zunächst zehn Kandidaten zu suchen und anschließend die drei besten mit einem Cross-Encoder auszuwählen?**

## Merksatz

**Die Kontextgröße beeinflusst den Tokenverbrauch und damit die Kosten einer RAG-Anfrage. Entscheidend ist nicht, möglichst viele Chunks zu übergeben, sondern ausreichend relevante Informationen mit möglichst wenig unnötigem Kontext bereitzustellen.**
