# Station 01: Unsere erste RAG-Pipeline

## Lernziel

Du entwickelst eine vollständige, einfache RAG-Pipeline. Du lernst, wie wir mithilfe von Embeddings relevante Informationen finden und einem Sprachmodell als Kontext für die Beantwortung einer Frage bereitstellen.

## Hintergrund

**Retrieval-Augmented Generation (RAG)** kombiniert zwei Aufgaben:

1. **Retrieval:** Relevante Informationen aus einer Wissensbasis suchen.
2. **Generation:** Mit einem Sprachmodell eine Antwort auf Grundlage dieser Informationen erzeugen.

Das Sprachmodell muss die gesuchte Information dadurch nicht aus seinem Trainingswissen kennen. Wir stellen sie ihm zur Laufzeit bereit.

Unsere Wissensbasis besteht zunächst aus nur fünf kurzen Texten über die fiktive Orbit API.

## Was machen wir?

### 1. Embeddings erzeugen

Wir verwenden das OpenAI-Modell `text-embedding-3-small`.

Es wandelt jeden unserer fünf Texte und die Benutzerfrage in einen numerischen Vektor um.

Ein solcher Vektor wird als **Embedding** bezeichnet. Er repräsentiert Eigenschaften des Textinhalts in einem mehrdimensionalen Vektorraum.

Die Idee: Texte mit ähnlicher Bedeutung sollen im Vektorraum möglichst nahe beieinanderliegen.

### 2. Ähnlichkeit berechnen

Wir vergleichen das Embedding der Frage mit jedem Dokument-Embedding.

Dafür verwenden wir die **Kosinusähnlichkeit (Cosine Similarity)**:

$$
\operatorname{sim}(a,b)=
\frac{a\cdot b}{\|a\|\|b\|}
$$

Sie misst die Ähnlichkeit der Richtungen zweier Vektoren.

Da die verwendeten OpenAI-Embeddings bereits auf die Länge 1 normiert sind, genügt für unsere Berechnung das Skalarprodukt.

Je größer die Kosinusähnlichkeit, desto ähnlicher sind die Vektoren.

### 3. Retrieval durchführen

Wir wählen das Dokument mit der höchsten Kosinusähnlichkeit aus.

Dazu benötigen wir noch keine Vektordatenbank. Bei nur fünf Dokumenten können wir sämtliche Ähnlichkeiten direkt mit NumPy berechnen.

### 4. Antwort generieren

Wir übergeben dem Sprachmodell `gpt-4.1-mini` zwei Informationen:

- die ursprüngliche Benutzerfrage
- den gefundenen Text als Kontext

Zusätzlich weisen wir das Modell an, ausschließlich anhand dieses Kontexts zu antworten.

## Was zeigt der Output?

Die Embedding-API verarbeitet insgesamt **66 Input-Tokens**.

Sie liefert sechs Vektoren mit jeweils **1536 Dimensionen**:

- fünf Dokument-Embeddings
- ein Embedding der Benutzerfrage

Die berechneten Ähnlichkeiten lauten:

| Dokumentinhalt | Kosinusähnlichkeit |
|---|---:|
| Webhook-Retries: 72 Stunden | **0,8321** |
| Access Tokens: 60 Minuten | 0,5134 |
| Telemetrie-Aufbewahrung: 90 Tage | 0,4752 |
| API-Limit: 1000 Requests/Minute | 0,5091 |
| Telemetrie-Export: CSV und JSON | 0,3271 |

Das Dokument über Webhook-Retries erreicht die höchste Ähnlichkeit.

Unser Retrieval liefert deshalb:

```text
Orbit retries failed webhook deliveries for 72 hours.
```

Das Sprachmodell generiert daraus die Antwort:

```text
Orbit versucht fehlgeschlagene Webhook-Zustellungen
für 72 Stunden erneut.
```

Damit haben wir unsere erste vollständige RAG-Pipeline ausgeführt.

## Warum ist das für RAG wichtig?

Wir haben die grundlegenden Verarbeitungsschritte eines RAG-Systems kennengelernt:

```text
Dokumente                    Benutzerfrage
    |                              |
    v                              v
Dokument-Embeddings          Frage-Embedding
    |                              |
    +-------------+----------------+
                  |
                  v
          Ähnlichkeitssuche
                  |
                  v
          Relevantes Dokument
                  |
                  v
        Frage + Kontext an LLM
                  |
                  v
                Antwort
```

Dieses Prinzip bleibt auch bei größeren RAG-Systemen erhalten.

Später ersetzen wir die manuelle Suche durch eine Vektordatenbank und erweitern das Retrieval um zusätzliche Verfahren.

## Grenzen unserer ersten Pipeline

Unsere Implementierung ist bewusst einfach:

- Wir durchsuchen nur fünf kurze Texte.
- Wir wählen ausschließlich das ähnlichste Dokument aus.
- Wir prüfen noch nicht systematisch, ob die Antwort korrekt ist.
- Wir speichern die Embeddings noch nicht dauerhaft.

Außerdem gilt: Eine hohe Kosinusähnlichkeit bedeutet nicht automatisch, dass ein Dokument die Frage tatsächlich beantwortet.


## Eigenes Experiment

Verändere die Frage so, dass unsere fünf Dokumente keine passende Antwort enthalten.

Beobachte, welches Dokument trotzdem als ähnlichstes gefunden wird und wie das Sprachmodell darauf reagiert.

## Merksatz

**RAG verbindet die Suche nach relevanten Informationen mit der Antwortgenerierung durch ein Sprachmodell. Das Retrieval liefert den Kontext, das Sprachmodell formuliert daraus die Antwort.**
