"""Station 4: Dense Search, BM25 und Rank Fusion vergleichen.

Vorher Station 3 mit --index starten.
Start: uv run python -m stations.04_hybrid
"""

from training_rag.pipeline import (bm25_search, dense_search, get_client,
                                  get_collection, load_users, reciprocal_rank_fusion)

QUESTIONS = ["How long does a cursor remain valid?", "AUTH-104"]


def main() -> None:
    collection = get_collection()
    client = get_client()
    user = load_users()["anonymous"]
    for question in QUESTIONS:
        dense = dense_search(collection, client, question, user, top_k=5)
        lexical = bm25_search(collection, question, user, top_k=5)
        fused = reciprocal_rank_fusion([dense, lexical])
        print(f"\nFRAGE: {question}")
        print("Dense:  ", [hit["id"] for hit in dense[:3]])
        print("BM25:   ", [hit["id"] for hit in lexical[:3]])
        print("RRF:    ", [(cid, round(score, 4)) for cid, score in fused[:3]])
        print("RRF kombiniert Ränge, keine verschieden skalierten Scores.")


if __name__ == "__main__":
    main()
