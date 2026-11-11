"""
Station 12: Re-Ranking mit einem Cross-Encoder

Lernziel:
Gefundene Chunks mit einem Cross-Encoder
neu bewerten und sortieren.

Ablauf:
1. Dense Retrieval liefert 10 Kandidaten.
2. Cross-Encoder bewertet Frage und Chunks gemeinsam.
3. Kandidaten nach Relevanz sortieren.
4. Die drei besten Treffer anzeigen.

Voraussetzungen:
uv add sentence-transformers

Der Chroma-Index aus Station 05 muss existieren.

Start:
uv run python -m stations.12_reranking
"""

from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# 1. Konfiguration

PROJECT_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_DIR / "data" / "chroma_05"

COLLECTION_NAME = "teralune_metadata"

EMBEDDING_MODEL = "text-embedding-3-small"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

QUESTION = "How long is an Orbit 3 access token valid?"

TOP_K_RETRIEVAL = 10
TOP_K_FINAL = 3

load_dotenv(PROJECT_DIR / ".env")


# 2. Dense Retrieval


def dense_search(collection, client, question, top_k=10):
    """Sucht die ähnlichsten Chunks über OpenAI-Embeddings."""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question,
    )

    question_vector = response.data[0].embedding

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=top_k,
    )

    return [
        {
            "id": chunk_id,
            "text": text,
        }
        for chunk_id, text in zip(
            results["ids"][0],
            results["documents"][0],
        )
    ]


def rerank(reranker, question, hits):
    """
    Bewertet gefundene Chunks mit einem Cross-Encoder.

    Frage und Chunk werden gemeinsam verarbeitet.
    Die Treffer werden anschließend nach ihrem
    Relevanz-Score sortiert.
    """

    # TODO 1:
    # Erstelle für jeden Chunk ein Paar aus Frage und Text.
    #
    # Beispiel:
    # (question, hit["text"])
    #
    # Speichere alle Paare in einer Liste namens pairs.

    # pairs = ...

    # TODO 2:
    # Lass den Cross-Encoder alle Paare bewerten.
    #
    # Verwende:
    # reranker.predict(pairs)
    #
    # Speichere das Ergebnis in scores.
    #
    # Ergänze anschließend bei jedem Treffer
    # den berechneten Score unter hit["score"].
    #
    # Tipp:
    # for hit, score in zip(hits, scores):
    #     ...

    # TODO 3:
    # Sortiere hits absteigend nach hit["score"].
    #
    # Verwende sorted() mit key und reverse=True.
    #
    # Gib die sortierte Liste zurück.

    return []


# 4. Ausgabe


def show_results(title, hits):
    """Zeigt die Reihenfolge der Suchergebnisse."""

    print(f"\n{title}")

    for position, hit in enumerate(hits, start=1):
        score = hit.get("score")

        if score is None:
            print(f"  {position:2}. {hit['id']}")
        else:
            print(f"  {position:2}. {hit['id']} Score: {score:.3f}")


# 5. Hauptprogramm


def main():

    client = OpenAI()

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = chroma.get_collection(name=COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        raise SystemExit("Collection fehlt. Zuerst Station 05 indexieren.")

    if collection.count() == 0:
        raise SystemExit("Collection ist leer.")

    print("RE-RANKING MIT CROSS-ENCODER")
    print("Frage:", QUESTION)

    # Dense Retrieval: 10 Kandidaten suchen.
    hits = dense_search(
        collection,
        client,
        QUESTION,
        top_k=TOP_K_RETRIEVAL,
    )

    show_results(
        "VOR DEM RE-RANKING (Dense Retrieval)",
        hits,
    )

    # TODO 1 bis 3:
    # Aktiviere nach der Implementierung von rerank()
    # den folgenden Programmteil.

    # reranker = CrossEncoder(RERANKER_MODEL)
    #
    # ranked_hits = rerank(
    #     reranker,
    #     QUESTION,
    #     hits,
    # )
    #
    # show_results(
    #     "NACH DEM RE-RANKING (Cross-Encoder)",
    #     ranked_hits[:TOP_K_FINAL],
    # )


if __name__ == "__main__":
    main()
