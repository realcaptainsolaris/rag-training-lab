# Station 13: HTML und CSV parsen

## Lernziel

Du lernst, wie wir unterschiedliche Dokumentformate für eine RAG-Pipeline in Text umwandeln.

Wir untersuchen zwei Beispiele:

1. HTML-Dokumente mit strukturierten Textinhalten.
2. CSV-Dateien mit tabellarischen Daten.

Dabei unterscheiden wir zwischen **Parsing** und **Chunking**.

## Hintergrund

Bisher haben wir hauptsächlich Markdown-Dokumente verarbeitet.

In realen RAG-Systemen liegen Informationen jedoch in unterschiedlichen Formaten vor, beispielsweise HTML, PDF, Word oder CSV.

Bevor wir solche Informationen vektorisieren können, müssen wir ihre Inhalte extrahieren und sinnvoll aufbereiten.

Diesen Verarbeitungsschritt nennen wir **Parsing**.

Dabei geht es nicht nur darum, möglichst viel Text zu gewinnen.

Entscheidend ist, dass die Informationen anschließend noch verständlich sind.

## Was machen wir?

Wir verarbeiten zwei Dateien aus unserem Teralune-Korpus:

| Datei | Format | Inhalt |
|---|---|---|
| D006.html | HTML | Fehlerkatalog für Authentifizierung und API |
| D007.csv | CSV | Produktpläne und ihre Grenzwerte |

### 1. HTML parsen

Für HTML verwenden wir die Python-Standardbibliothek `html.parser`.

Unsere Klasse `TextExtractor` sammelt die Textinhalte zwischen den HTML-Tags.

Die Tags selbst werden nicht übernommen.

Aus:

```html
<h2>Error identifiers</h2>
<p>AUTH-104 means access token expired.</p>
```

wird:

```text
Error identifiers
AUTH-104 means access token expired.
```

Der extrahierte Text kann anschließend weiterverarbeitet werden.

### 2. CSV parsen

Bei CSV-Dateien gehen wir anders vor.

Hier soll jede Tabellenzeile einen eigenen Textblock ergeben.

Dabei behalten wir die Spaltennamen bei.

Beispiel:

```csv
plan,devices_per_organization
Team,1000
```

Daraus wird:

```text
plan: Team
devices_per_organization: 1000
```

Warum ist das sinnvoll?

Der isolierte Wert `1000` besitzt kaum Bedeutung.

Erst durch den Spaltennamen wird deutlich, dass es sich um die Anzahl erlaubter Geräte pro Organisation handelt.

## Was zeigt der Output?

### HTML: Authentication Error Catalogue

Unser Parser extrahiert den Text aus `D006.html`.

Darin finden wir beispielsweise:

```text
AUTH-104 means access token expired.
AUTH-140 means required scope missing.
AUTH-141 means workspace mismatch.
```

Die Fehlerkennungen bleiben erhalten.

Das ist wichtig, weil Benutzer später gezielt nach einer Kennung wie `AUTH-140` suchen könnten.

Allerdings fällt im Output etwas auf:

```text
Authentication Error Catalogue
Authentication Error Catalogue
```

Der Titel erscheint zweimal.

Unser einfacher Parser übernimmt sämtliche Textabschnitte, einschließlich des Seitentitels und der sichtbaren Überschrift.

Er erkennt nicht, dass beide denselben Inhalt beschreiben.

Außerdem gehen Informationen über die ursprüngliche HTML-Struktur verloren.

### CSV: Produktpläne

Aus `D007.csv` entstehen drei Textblöcke.

Ein Beispiel:

```text
Datensatz 2

plan: Team
devices_per_organization: 1000
retention_days: 180
workspaces_per_organization: 5
```

Alle Werte eines Produktplans bleiben zusammen.

Damit könnte ein RAG-System später beispielsweise folgende Frage beantworten:

> Wie viele Geräte unterstützt der Team-Plan?

Der passende Textblock enthält sowohl den Plannamen als auch den zugehörigen Grenzwert.

Insgesamt erzeugt unser Parser **drei CSV-Textblöcke**.

## Parsing und Chunking unterscheiden

Diese beiden Schritte erfüllen unterschiedliche Aufgaben.

**Parsing** extrahiert Informationen aus einem Dateiformat und überführt sie in eine nutzbare Darstellung.

**Chunking** zerlegt diese Informationen anschließend in Einheiten für das Retrieval.

```text
       HTML / CSV
           |
           v
         Parsing
           |
           v
    Aufbereiteter Text
           |
           v
         Chunking
           |
           v
         Chunks
           |
           v
        Embeddings
           |
           v
      Vektordatenbank
```

Unsere CSV-Textblöcke könnten direkt als Chunks verwendet werden.

Bei längeren HTML-Dokumenten wäre dagegen möglicherweise eine weitere Aufteilung sinnvoll.

## Warum ist das für RAG wichtig?

Die Qualität des Retrievals hängt auch von der Qualität der aufbereiteten Daten ab.

Wenn beim Parsing wichtige Informationen verloren gehen, können spätere Verarbeitungsschritte sie nicht zuverlässig wiederherstellen.

Bei Tabellen ist besonders wichtig, dass Werte ihren Spalten und Datensätzen zugeordnet bleiben.

Bei HTML kann es sinnvoll sein, Überschriften, Absätze und andere Strukturelemente zu erhalten.

Unser HTML-Parser ist bewusst einfach gehalten.

Produktive RAG-Systeme benötigen häufig aufwendigere Parser, die beispielsweise Navigationselemente, JavaScript und doppelte Inhalte entfernen und gleichzeitig die Dokumentstruktur bewahren.

## Eigenes Experiment

Untersuche die HTML-Datei `D006.html`.

Vergleiche ihre ursprüngliche Struktur mit dem extrahierten Text.

Überlege, welche Informationen verloren gehen.

Betrachte anschließend die CSV-Ausgabe.

**Was würde passieren, wenn wir alle CSV-Werte ohne Spaltennamen und ohne Trennung der Datensätze aneinanderhängen würden?**

## Merksatz

**Parsing macht Dokumentinhalte für die weitere Verarbeitung zugänglich. Chunking bestimmt anschließend, in welchen Einheiten diese Inhalte durchsucht werden. Eine gute RAG-Pipeline muss beide Schritte berücksichtigen.**
