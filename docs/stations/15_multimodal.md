# Station 15: Multimodales RAG mit Bildern

## Lernziel

Du lernst, wie Bilder für eine RAG-Pipeline durchsuchbar gemacht werden können.

Dazu verwenden wir ein Vision-Modell, das Bilder beschreibt. Anschließend erzeugen wir Embeddings dieser Beschreibungen und speichern sie in Chroma.

**Wichtig:** Wir erzeugen Text-Embeddings der Bildbeschreibungen, keine direkten Bild-Embeddings.

## Hintergrund

Bisher haben wir hauptsächlich Textdokumente verarbeitet.

In der Praxis enthalten Wissensdatenbanken jedoch auch Bilder, beispielsweise Architekturdiagramme, Screenshots oder Monitoring-Dashboards.

Solche Informationen können für die Beantwortung technischer Fragen wichtig sein.

Ein möglicher Ansatz besteht darin, Bilder zunächst mit einem Vision-Modell in Text zu übersetzen.

Die entstandenen Beschreibungen können anschließend mit unserer bisherigen RAG-Technik verarbeitet werden.

Dieses Verfahren verbindet Bildverarbeitung mit textbasiertem Retrieval.

## Was machen wir?

Wir verwenden drei Bilder aus unserer Orbit-Umgebung:

| Bild | Inhalt |
|---|---|
| Bild 1 | Architektur der Orbit API |
| Bild 2 | Fehlerbehebung bei HTTP 403 |
| Bild 3 | Monitoring-Dashboard mit Leistungsmetriken |

Unsere Pipeline besteht aus zwei Phasen.

### Phase 1: Bilder indexieren

```text
       PNG-Dateien
            |
            v
       Vision-Modell
            |
            v
     Bildbeschreibungen
            |
            v
       Text-Embeddings
            |
            v
           Chroma
```

Das Vision-Modell `gpt-4.1-mini` analysiert jedes Bild.

Wir bitten es, wichtige Beschriftungen, Fehlermeldungen, Kennzahlen und sichtbare Zusammenhänge zu beschreiben.

Anschließend erzeugen wir mit `text-embedding-3-small` einen Vektor für jede Beschreibung.

In Chroma speichern wir:

| Bestandteil | Gespeicherter Wert |
|---|---|
| ID | Eindeutige Bild-ID |
| Dokument | Generierte Bildbeschreibung |
| Embedding | Vektor der Beschreibung |
| Metadaten | Originaldateiname |

Die eigentlichen PNG-Dateien bleiben im Dateisystem.

### Phase 2: Bilder suchen

```text
          Textfrage
              |
              v
        Text-Embedding
              |
              v
            Chroma
              |
              v
    Ähnlichste Beschreibung
              |
              v
       Zugehöriges Bild
```

Bei der Suche muss das Vision-Modell nicht erneut aufgerufen werden.

Wir vergleichen ausschließlich Text-Embeddings.

## Was zeigt der Output?

### 1. Architekturdiagramm

Die erste Frage lautet:

> Which image explains the architecture of the Orbit API?

Chroma findet das Architekturdiagramm mit einer Distanz von **0,262**.

Die gespeicherte Beschreibung enthält unter anderem den API Gateway sowie den Authentication Service, Telemetry Service und Data Service.

Das Vision-Modell hat damit wesentliche Bestandteile und Beziehungen des Diagramms in Text übertragen.

### 2. Fehlende API-Berechtigung

Die zweite Frage lautet:

> Which image shows a missing API permission?

Chroma findet den Screenshot zur HTTP-403-Fehlerbehebung.

Distanz: **0,471**

Die Bildbeschreibung enthält die entscheidende Information:

```text
HTTP 403 Forbidden
Missing scope: telemetry:write
```

Dadurch kann das System den Screenshot anhand seines fachlichen Inhalts finden.

### 3. Erhöhte Latenz nach einem Deployment

Die dritte Frage lautet:

> Which image shows increased latency after a deployment?

Chroma findet das Monitoring-Dashboard.

Distanz: **0,468**

Die Beschreibung nennt das Deployment `v3.2.0` und den anschließenden Anstieg der Latenz von ungefähr 150 auf 300 Millisekunden.

Das zeigt einen Vorteil der Bildbeschreibung: Nicht nur einzelne Beschriftungen, sondern auch Zusammenhänge aus einem Diagramm können für die Suche nutzbar werden.

### 4. Hat das Deployment einen Ausfall verursacht?

Die vierte Frage lautet:

> Which image shows that a deployment caused an API outage?

Auch hier findet Chroma das Monitoring-Dashboard.

Distanz: **0,452**

Allerdings enthält die Bildbeschreibung keinen Nachweis dafür, dass das Deployment einen API-Ausfall verursacht hat.

Sie beschreibt lediglich einen zeitlichen Zusammenhang zwischen dem Deployment und erhöhten Fehler- und Latenzwerten.

**Zeitliche Korrelation ist kein Beweis für Kausalität.**

Außerdem zeigen die beschriebenen Metriken keinen vollständigen Ausfall.

Das Suchergebnis ist thematisch passend, bestätigt aber nicht die Behauptung in der Frage.

## Warum ist das für RAG wichtig?

Unser Experiment zeigt, dass wir Bilder mithilfe ihrer Textbeschreibungen in eine bestehende RAG-Pipeline integrieren können.

Der Ansatz hat allerdings Grenzen.

**1. Die Bildbeschreibung ist eine Interpretation.**

Das Vision-Modell kann wichtige Details übersehen, Zahlen falsch ablesen oder Zusammenhänge falsch interpretieren.

**2. Die Suche kennt nur die Beschreibung.**

Informationen, die nicht in der Beschreibung enthalten sind, stehen dem textbasierten Retriever nicht zur Verfügung.

**3. Ein passender Treffer beweist keine Aussage.**

Die vierte Frage zeigt, dass semantische Ähnlichkeit nicht mit faktischer Bestätigung gleichzusetzen ist.

Eine Alternative sind multimodale Embedding-Modelle, die Bilder direkt in einen Vektorraum abbilden können.

Unser Beispiel verwendet dagegen bewusst den einfacheren Weg über Textbeschreibungen.

## Eigenes Experiment

Verändere die Suchfragen.

Teste insbesondere Fragen zu konkreten Beschriftungen, Kennzahlen oder Beziehungen im Monitoring-Dashboard.

Vergleiche anschließend die Antworten mit der tatsächlich gespeicherten Bildbeschreibung.

Überlege:

**Was passiert, wenn das Vision-Modell eine wichtige Information im Bild nicht erkennt oder falsch beschreibt?**

## Merksatz

**Bilder können durch automatisch erzeugte Textbeschreibungen für RAG durchsuchbar werden. Die Qualität der Suche hängt dann wesentlich davon ab, wie vollständig und korrekt diese Beschreibungen sind.**



## Weitere Verfahren für multimodales RAG

Neben der Suche über automatisch erzeugte Bildbeschreibungen gibt es weitere Ansätze. **Multimodale Embedding-Modelle** wie CLIP können Bilder und Texte direkt in einen gemeinsamen Vektorraum abbilden. Dadurch lassen sich Bilder anhand von Textfragen suchen, ohne sie vorher beschreiben zu müssen. Eine weitere Möglichkeit ist **OCR (Optical Character Recognition)**, um Texte aus Screenshots, Diagrammen oder eingescannten Dokumenten zu extrahieren. Bei komplexen Dokumenten können Layout-Analyse und spezialisierte Dokumentmodelle zusätzlich Tabellen, Überschriften und räumliche Beziehungen berücksichtigen. Schließlich können **multimodale LLMs** die gefundenen Originalbilder direkt als Kontext erhalten und Fragen dazu beantworten. In der Praxis werden diese Verfahren häufig kombiniert, beispielsweise Text-Embeddings für die erste Suche und ein Vision-Modell zur anschließenden Analyse der gefundenen Bilder.
