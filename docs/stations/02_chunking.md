# Station 02: Dokumente in Chunks zerlegen

## Lernziel

Du lernst drei Chunking-Strategien kennen und verstehst, wie sich die Wahl der Chunk-Grenzen auf die Verarbeitung von Dokumenten in einem RAG-System auswirkt.

## Hintergrund

In Station 01 bestand unsere Wissensbasis aus fünf kurzen Sätzen. In der Praxis müssen RAG-Systeme jedoch häufig umfangreiche Dokumente verarbeiten.

Deshalb zerlegen wir Dokumente in kleinere Textabschnitte, sogenannte **Chunks**.

Jeder Chunk kann später einzeln in ein Embedding umgewandelt und in einer Vektordatenbank gespeichert werden.

Das Ziel besteht darin, relevante Informationen möglichst gezielt wiederzufinden, ohne bei jeder Anfrage vollständige Dokumente verarbeiten zu müssen.

Die Wahl der Chunk-Größe und der Chunk-Grenzen beeinflusst dabei die Qualität des Retrievals.

Chunking ist eine der größten Herausforderungen bei der Entwicklung von RAG-Systemen. Viele verschiedene Chunking-Strategien wurden in der Forschung untersucht. In der Praxis werden häufig mehrere Verfahren kombiniert.

Wir konzentrieren uns auf drei einfache Strategien, die wir in Python implementieren können.


## Was machen wir?

Wir laden das Markdown-Dokument `D022.md` aus unserem Teralune-Korpus.

Das Dokument behandelt Pagination und Cursor-Verarbeitung in der Orbit API und enthält **3978 Zeichen**.

Anschließend vergleichen wir drei Chunking-Strategien.

### 1. Fixed Size Chunking

Wir zerlegen das Dokument in Abschnitte mit maximal 500 Zeichen.

Die Grenzen werden unabhängig vom Inhalt gesetzt.

**Vorteil:** Einfach zu implementieren und vorhersehbare Chunk-Größen.

**Nachteil:** Wörter, Sätze oder zusammengehörige Informationen können an beliebigen Stellen getrennt werden.

### 2. Chunking mit Overlap

Wir verwenden ebenfalls 500 Zeichen pro Chunk, lassen benachbarte Chunks aber um 100 Zeichen überlappen.

```text
Chunk 1: Zeichen   0 bis 499
Chunk 2: Zeichen 400 bis 899
Chunk 3: Zeichen 800 bis 1299
```

Dadurch erscheinen Informationen an den Chunk-Grenzen in zwei benachbarten Abschnitten.

**Vorteil:** Zusammenhänge an Chunk-Grenzen bleiben eher erhalten.

**Nachteil:** Text wird mehrfach gespeichert und verarbeitet. Das erhöht den Speicherbedarf und gegebenenfalls die Kosten für Embeddings.

### 3. Structure Chunking

Markdown-Dokumente besitzen eine erkennbare Struktur durch Überschriften.

Wir nutzen die Überschriften `#`, `##` und `###`, um neue Chunks zu beginnen.

**Vorteil:** Inhaltlich zusammengehörige Abschnitte bleiben eher erhalten.

**Nachteil:** Die Chunk-Größen können stark variieren. Sehr lange Abschnitte müssten gegebenenfalls zusätzlich aufgeteilt werden.

Unsere Implementierung ist bewusst vereinfacht und berücksichtigt beispielsweise keine verschachtelte Überschriftenhierarchie.

## Was zeigt der Output?

Bei einer Chunk-Größe von 500 Zeichen und einem Overlap von 100 Zeichen erhalten wir:

| Strategie | Anzahl Chunks |
|---|---:|
| Fixed Size | 8 |
| Mit Overlap | 10 |
| Strukturorientiert | 6 |

Beim Fixed Size Chunking endet der erste Chunk mitten im Wort:

```text
... can silently splice two different res
```

Beim Chunking mit Overlap beginnt der zweite Chunk mit:

```text
ry. A consumer that changes the device filter ...
```

Die überlappenden Zeichen sorgen dafür, dass die vollständige Textstelle in beiden Chunks enthalten sein kann.

Beim Structure Chunking entstehen dagegen Abschnitte entlang der Markdown-Überschriften.

Beispielsweise beginnt ein Chunk mit:

```markdown
## Cursor traversal
```

und enthält den zugehörigen Abschnitt bis zur nächsten erkannten Überschrift.

Auffällig ist außerdem, dass die oberste Überschrift `# Pagination and cursors` einen eigenen, sehr kurzen Chunk bildet.

Das zeigt: Auch strukturorientiertes Chunking liefert nicht automatisch optimale Ergebnisse.

## Warum ist das für RAG wichtig?

Chunking beeinflusst unmittelbar, welche Informationen ein Retriever später finden kann.

**Zu kleine Chunks** können wichtige Zusammenhänge verlieren.

**Zu große Chunks** enthalten möglicherweise viele irrelevante Informationen und erhöhen den Kontextumfang bei der Antwortgenerierung.

**Overlap** kann helfen, Informationen an Chunk-Grenzen zu bewahren, erzeugt aber redundante Daten.

**Strukturorientiertes Chunking** kann semantisch zusammengehörige Informationen erhalten, benötigt jedoch geeignete Regeln für unterschiedliche Dokumenttypen.

Es gibt deshalb keine Chunking-Strategie, die für sämtliche Dokumente optimal ist.

In produktiven RAG-Systemen werden häufig mehrere Verfahren kombiniert.

## Eigenes Experiment

Verändere die Parameter:

```python
CHUNK_SIZE = 300
OVERLAP = 50
```

Führe das Skript erneut aus und vergleiche die Anzahl und Inhalte der erzeugten Chunks.

Überlege anschließend, welche Strategie sich am besten für technische Dokumentation mit Überschriften eignet.

## Merksatz

**Chunking ist mehr als das Zerlegen von Text. Die gewählten Chunk-Grenzen beeinflussen, welche Informationen ein RAG-System später zuverlässig wiederfinden kann.**
