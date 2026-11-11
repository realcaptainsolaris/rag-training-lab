"""
Station 08: Retrieval-Evaluation mit Goldfragen
================================================

LERNZIEL
--------
Wir überprüfen, ob unsere Vektorsuche die richtigen Chunks findet.

Dazu verwenden wir Goldfragen:
Für jede Frage legen wir vorher fest, welcher Chunk
die benötigte Information enthält.

METRIK: HIT@3
-------------
Wir betrachten die ersten drei Suchergebnisse.

Ist der erwartete Chunk dabei?
    Ja   -> Hit = 1
    Nein -> Hit = 0

Am Ende berechnen wir den Anteil erfolgreicher Fragen.

WICHTIG
-------
Wir bewerten nur das Retrieval, nicht die LLM-Antwort.

Die Gold-Chunk-IDs müssen zum aktuellen Index passen.

START
-----
uv run python -m stations.08_evaluation
"""

from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# ============================================================
# 1. Vorbereitung
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = PROJECT_DIR / "data" / "chroma_05"
COLLECTION_NAME = "teralune_metadata"

TOP_K = 3

# Goldfragen mit dem jeweils erwarteten Chunk.
#
# Diese IDs beziehen sich auf unser Structure Chunking.
# Bei Änderungen am Chunking müssen wir sie überprüfen.

GOLD_QUESTIONS = [
    {
        "question": "How long does a cursor remain valid?",
        "gold_chunk": "D022_2",
    },
    {
        "question": "How long is an Orbit 3 access token valid?",
        "gold_chunk": "D002_1",
    },
    {
        "question": "What is the next_cursor field used for?",
        "gold_chunk": "D022_1",
    },
]

load_dotenv(PROJECT_DIR / ".env")

client = OpenAI()

chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma.get_collection(name=COLLECTION_NAME)


# ============================================================
# 2. Goldfragen auswerten
# ============================================================

hits = 0

for item in GOLD_QUESTIONS:
    question = item["question"]
    gold_chunk = item["gold_chunk"]

    # Suchfrage in einen Embedding-Vektor umwandeln.

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question,
    )

    question_vector = response.data[0].embedding

    # Die drei ähnlichsten Chunks suchen.

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=TOP_K,
    )

    found_ids = results["ids"][0]

    # ========================================================
    # 3. HIT@3 berechnen
    # ========================================================

    # Wir vergleichen die gefundenen Chunk-IDs
    # mit dem erwarteten Gold-Chunk.
    #
    # Ist er unter den ersten drei Treffern,
    # gilt die Frage als erfolgreich.

    hit = gold_chunk in found_ids

    if hit:
        hits += 1

    print("\nFRAGE:", question)
    print("Erwartet:", gold_chunk)
    print("Gefunden:", found_ids)
    print("Hit@3:", int(hit))


# ============================================================
# 4. Gesamtergebnis
# ============================================================

hit_rate = hits / len(GOLD_QUESTIONS)

print("\n" + "=" * 60)
print("RETRIEVAL-EVALUATION")
print("=" * 60)

print("Goldfragen:", len(GOLD_QUESTIONS))
print("Erfolgreich:", hits)
print(f"Hit@3: {hit_rate:.1%}")
