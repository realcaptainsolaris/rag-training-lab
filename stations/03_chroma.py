"""Station 3: Persistenten Chroma-Index aufbauen und anschließend suchen.

Start: uv run python -m stations.03_chroma --index
       uv run python -m stations.03_chroma
"""

import argparse

from training_rag.pipeline import build_index, dense_search, get_client, get_collection, load_users

QUESTION = "How long is an Orbit 3 access token valid?"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", action="store_true", help="Index neu aufbauen")
    args = parser.parse_args()
    if args.index:
        collection, chunks = build_index()
        print(f"Indexiert: {len(chunks)} Chunks aus dem Teralune-Mini-Corpus")
    else:
        collection = get_collection()
    print(f"Persistente Chroma-Einträge: {collection.count()}")
    client = get_client()
    user = load_users()["anonymous"]
    for label, current in [("Ohne Versionsfilter", False), ("Nur 3.0/current", True)]:
        results = dense_search(collection, client, QUESTION, user,
                               top_k=3, version="3.0" if current else None,
                               current_only=current)
        print(f"\n{label}:")
        for hit in results:
            meta = hit["metadata"]
            print(f"  {hit['id']} | Version={meta['version']} | Status={meta['status']} | Distanz={hit['distance']:.3f}")


if __name__ == "__main__":
    main()
