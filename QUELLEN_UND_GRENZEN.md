# Dokumentauswahl und Grenzen der Rohfassung

## Herkunft

Die 16 Quelldokumente wurden unverändert aus dem bereitgestellten
`telarune_corpus.zip` (Teralune Corpus 1.0) übernommen. Dokumentmetadaten
wurden unverändert aus `source/document_manifest.json` ausgewählt.
Die 15 Evaluationsfragen wurden unverändert aus `evaluation/smoke_questions.jsonl`
ausgewählt. Das separat übergebene `evidence_mapping.json` wurde auf die
zugehörigen Evidenz-IDs reduziert, nicht neu geschätzt.

## Auswahlprinzip

- D001, D002, D003, D004, D005, D012, D033 und D034: Fakten, Generationen,
  Versionierung und historische Kontraste.
- D022: Struktur-Chunking (Cursor, Filter und Laufzeit).
- D006 (HTML) und D007 (CSV): Parsing unterschiedlicher Quellformate.
- D008 und D037: kundenspezifische Zugriffsgrenzen, widersprüchliche Inhalte.
- D009 und D010: INTERNAL und RESTRICTED zum ACL-Vergleich.
- D011: unreviewte importierte Receiver-Notiz mit Prompt-Injection-Testtext.

## Qualitätsgrenzen

- 44 Chunks entstehen aus 16 Dokumenten durch das implementierte Markdown-
  Struktur-Chunking bzw. durch einfaches HTML-/CSV-Parsing.
- Für elf `answer`-Fragen liegen exakte Goldzuordnungen vor. Die übrigen vier
  Fragen prüfen `deny`, `clarify` und `no_answer` und sind **nicht** Teil
  aggregierter Retrieval-Metriken.
- Die Metrikberechnung ist nicht durch einen echten OpenAI/Chroma-Lauf
  validiert. Für Aussagen über Trefferquoten braucht es die Generalprobe.
- Die Unterlagen enthalten fiktive Daten. Das Berechtigungsbeispiel ist
  keine vollständige Sicherheitsarchitektur.
- Der Mini-Corpus wird zu Schulungszwecken komplett verteilt. Die im Index
  demonstrierten ACLs können deshalb **keine lokale Dateivertraulichkeit**
  garantieren; sie erklären lediglich die erforderlichen Filter in einer
  serverseitigen produktiven RAG-Architektur.
