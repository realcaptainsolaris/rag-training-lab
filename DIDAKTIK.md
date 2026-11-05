# Dozentennotiz: Verbindliche Demos und Zeitgrenzen

| Station | Zeit | Pflichtdemonstration | Buchbezug |
| --- | ---: | --- | --- |
| 1 | 45 min | Mini-RAG mit 5 Fakten | Kapitel 1 |
| 2 | 70 min | Cursor-Dokument: Fixed/Overlap/Struktur | Kapitel 2 |
| 3 | 90 min | Indexieren, Wiederverwenden, Versionsfilter | Kapitel 3 |
| 4 | 105 min | Dense gegen BM25, RRF; Reranking visualisieren | Kapitel 4 |
| 5 | 70 min | Quellen und eine unbeantwortbare Frage | Kapitel 5 |
| 6 | 90 min | Goldfragen, Hit/Recall/MRR; Fehlertypen | Kapitel 6 |
| 7 | 95 min | ACL-Szenario; Security/Privacy/Cloud/Cost als Folien | Kapitel 7 |
| 8 | 45 min | Szenarien: Standard, Agentic, Graph, multimodal | Advanced |

## Methodische Leitplanken

- **Alle Themen sind Pflicht, alle Experimente optional.** Der rote Faden ist
  der wachsende Prototyp, keine Serie vollständiger Code-Reviews.
- Reranking wird im Pflichtprogramm als Konzept und Rankingvergleich gezeigt.
  Der CrossEncoder aus dem Buch bleibt optional, weil lokale Modellgewichte
  bzw. PyTorch die Schulungsumgebung unnötig belasten können.
- Kein fachlich falscher Claim: Metadatenfilter erhöhen nicht die semantische
  Ähnlichkeit. Sie reduzieren Kandidaten anhand von Regeln.
- Kein Demo-Output erfinden: erst lokal mit API und realem Corpus testen.
- Keine Sicherheitsgarantien aus Prompt-Regeln ableiten.

## Zurückgestellter Punkt für die Generalprobe

Die sechs Programme mit OpenAI-/Chroma-Abhängigkeit benötigen noch reale
Integrationstests; speziell muss der ACL-Chroma-Filter im installierten
Versionsstand geprüft werden. Die Offline-Tests prüfen Daten, Zuordnungen,
Rechteprädikat und Metriken, nicht das produktive Chroma-Verhalten.
