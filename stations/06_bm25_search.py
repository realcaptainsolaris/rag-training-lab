"""
Station 06: Lexikalische Suche mit BM25

Lernziel:
Dokumente anhand ihrer Suchbegriffe durchsuchen.

Voraussetzung:
uv run python -m stations.05_chroma_filter --index

Start:
uv run python -m stations.06_bm25
"""

import re
from pathlib import Path

import chromadb

PROJECT_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_DIR / "data" / "chroma_05"
COLLECTION_NAME = "teralune_metadata"

QUESTIONS = [
    "How long does a cursor remain valid?",
    "next_cursor",
]


# 1. Tokenisierung


def tokenize(text):
    """Zerlegt Text in kleingeschriebene Suchbegriffe."""

    return re.findall(r"\w+", text.lower())


# 2. BM25-Suche


def bm25_search(collection, question, top_k=5):

    stored = collection.get(include=["documents"])

    documents = stored["documents"]
    ids = stored["ids"]

    if not documents:
        return []

    # TODO 1:
    # Tokenisiere alle Dokumente.
    # Verwende dafür die Funktion tokenize().
    #
    # Tipp: List Comprehension

    # tokenized_documents = [...]

    # TODO 2:
    # Erstelle einen BM25-Index.
    # Berechne die Scores für die tokenisierte Suchfrage.
    #
    # Tipp:
    # bm25 = BM25Okapi(...)
    # scores = bm25.get_scores(...)

    # TODO 3:
    # Sortiere die Treffer absteigend nach BM25-Score.
    #
    # Tipp: sorted() mit reverse=True

    # ranked = ...

    # results = []
    #
    # for chunk_id, document, score in ranked[:top_k]:
    #     if score <= 0:
    #         continue
    #
    #     results.append({
    #         "id": chunk_id,
    #         "text": document,
    #         "bm25": float(score),
    #     })
    #
    # return results

    return []


# 3. Hauptprogramm


def main():

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = chroma.get_collection(name=COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        raise SystemExit("Collection fehlt. Zuerst Station 05 indexieren.")

    print("BM25-SUCHE")
    print("Gespeicherte Chunks:", collection.count())

    for question in QUESTIONS:
        results = bm25_search(collection, question, top_k=5)

        print("\n" + "=" * 60)
        print("FRAGE:", question)

        if not results:
            print("Noch keine Treffer. TODOs bearbeiten.")
            continue

        for rank, hit in enumerate(results, start=1):
            print(f"\nRang {rank}")
            print("Chunk:", hit["id"])
            print("BM25-Score:", round(hit["bm25"], 3))
            print("Text:", hit["text"][:300])


if __name__ == "__main__":
    main()
