# Station 00: Was sind Tokens?

## Lernziel

Du verstehst, wie ein Tokenizer Text zerlegt, was Token-IDs sind und warum die Anzahl der Tokens nicht mit der Anzahl der Wörter übereinstimmt.

## Hintergrund

Sprachmodelle verarbeiten Text nicht unmittelbar als Wörter. Zunächst zerlegt ein **Tokenizer** den Text in kleinere Einheiten, sogenannte Tokens.

Ein Token kann beispielsweise sein:

- ein vollständiges Wort
- ein Wortteil
- ein Satzzeichen
- ein Leerzeichen zusammen mit einem Wortteil

Jedes Token erhält eine numerische **Token-ID**. Diese ID ist innerhalb des jeweiligen Tokenizers eindeutig.

Verschiedene Tokenizer können denselben Text unterschiedlich zerlegen. In dieser Station verwenden wir `cl100k_base` aus der Python-Bibliothek `tiktoken`.

Die Tokenisierung ist ein vorbereitender Schritt für die Verarbeitung durch Sprachmodelle. Sie ist noch keine semantische Analyse des Textes.

## Was machen wir?

Wir untersuchen zwei kurze Texte.

**1. Text tokenisieren**

Mit `tiktoken` zerlegen wir einen englischen Satz in Tokens und lassen uns die zugehörigen Token-IDs anzeigen.

**2. Tokens sichtbar machen**

Anschließend dekodieren wir die einzelnen Token-IDs. Dadurch sehen wir, aus welchen Textstücken der ursprüngliche Satz besteht.

**3. Wörter und Tokens vergleichen**

Wir untersuchen einen zweiten Satz mit einem zusammengesetzten Fachbegriff und vergleichen die Anzahl der Wörter mit der Anzahl der Tokens.

## Was zeigt der Output?

Beim ersten Satz:

```text
Hello, I am learning about RAG!
```

entstehen neun Tokens.

Interessant ist insbesondere der Fachbegriff `RAG`:

```text
432  : ' R'
1929 : 'AG'
```

Der Tokenizer zerlegt ihn in zwei Tokens. Das führende Leerzeichen gehört zum ersten Token.

Beim zweiten Satz erhalten wir:

```text
Text: Retrieval-Augmented Generation ist spannend!
Anzahl Wörter: 4
Anzahl Tokens: 11
```

Obwohl der Satz nur vier durch Leerzeichen getrennte Wörter enthält, benötigt der Tokenizer elf Tokens.

## Warum ist das für RAG wichtig?

Bei RAG arbeiten wir häufig mit Text-Chunks, Embeddings und Sprachmodellen.

Dabei spielt die Tokenanzahl eine wichtige Rolle:

- **Chunking:** Textabschnitte können anhand ihrer Tokenanzahl begrenzt werden.
- **Kontextfenster:** Modelle können nur eine begrenzte Anzahl von Tokens gleichzeitig verarbeiten.
- **Kosten:** Viele API-Anbieter berechnen die Nutzung anhand der verarbeiteten Tokens.

Deshalb reicht es nicht aus, lediglich Wörter oder Zeichen zu zählen.

## Eigenes Experiment

Verändere den Text im Skript und vergleiche die Ergebnisse für deutsche und englische Sätze, Fachbegriffe und zusammengesetzte Wörter.

Beobachte insbesondere, welche Wörter in mehrere Tokens zerlegt werden.

## Merksatz

**Ein Token ist nicht dasselbe wie ein Wort. Die Tokenanzahl hängt vom Text und vom verwendeten Tokenizer ab.**
