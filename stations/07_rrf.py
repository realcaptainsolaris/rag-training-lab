"""
Station 07: Reciprocal Rank Fusion (RRF)

Lernziel:
Zwei Rankings anhand ihrer Rangpositionen kombinieren.

Formel:
RRF-Beitrag = 1 / (k + Rang)

Start:
uv run python -m stations.07_rrf
"""

RRF_K = 60

bm25 = ["A", "B", "C"]
dense = ["B", "C", "A"]


def reciprocal_rank_fusion(rankings, k=60):

    scores = {}

    # TODO 1:
    # Durchlaufe alle Rankings und ihre Treffer.
    #
    # Verwende zwei verschachtelte for-Schleifen.
    # enumerate(..., start=1) liefert die Rangposition.

    # for ranking in rankings:
    #     for rank, chunk_id in enumerate(ranking, start=1):

    #         TODO 2:
    #         Berechne den RRF-Beitrag: 1 / (k + rank)
    #         Addiere ihn zum bisherigen Score des Chunks.
    #
    #         Tipp:
    #         scores.get(chunk_id, 0)

    # TODO 3:
    # Sortiere die Chunks absteigend nach ihrem RRF-Score.
    #
    # Tipp: sorted() mit key=...

    # ranked = ...

    return []


def main():
    print("RECIPROCAL RANK FUSION")

    print("\nBM25-Ranking:")
    for rank, chunk_id in enumerate(bm25, start=1):
        print(f"  {rank}. Chunk {chunk_id}")

    print("\nDense-Ranking:")
    for rank, chunk_id in enumerate(dense, start=1):
        print(f"  {rank}. Chunk {chunk_id}")

    fused = reciprocal_rank_fusion([bm25, dense], k=RRF_K)

    print("\nRRF-Ranking:")

    for rank, (chunk_id, score) in enumerate(fused, start=1):
        print(f"  {rank}. Chunk {chunk_id} | RRF: {score:.6f}")

    # TODO 4:
    # Prüfe, ob die Reihenfolge B, A, C herauskommt.


if __name__ == "__main__":
    main()
