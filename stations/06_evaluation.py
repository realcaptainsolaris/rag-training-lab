"""Station 6: Goldfragen und Retrieval-Metriken aus dem Teralune-Corpus.

Nur 'answer'-Fragen mit vollständiger exakter Chunk-Zuordnung bewerten.
Start: uv run python -m stations.06_evaluation
"""

import json

from training_rag.documents import PROJECT_DIR
from training_rag.metrics import calculate_metrics
from training_rag.pipeline import (
    dense_search,
    get_client,
    get_collection,
    is_visible,
    load_users,
)

DATA = PROJECT_DIR / "data" / "evaluation"
TOP_K = 5


def main() -> None:
    questions = [
        json.loads(line)
        for line in (DATA / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    mapping = json.loads((DATA / "evidence_mapping.json").read_text(encoding="utf-8"))
    users = load_users()
    collection = get_collection()
    ids = set(collection.get(include=[])["ids"])
    client = get_client()
    scores: list[dict[str, float]] = []
    excluded = 0

    for question in questions:
        if question["expected_behavior"] != "answer":
            excluded += 1
            continue
        evidence = [eid for eid, grade in question["relevance"].items() if grade > 0]
        if not evidence or any(
            mapping.get(eid, {}).get("status") != "exact" for eid in evidence
        ):
            excluded += 1
            continue
        gold = {cid for eid in evidence for cid in mapping[eid]["chunks"]}
        if not gold or not gold <= ids:
            excluded += 1
            continue
        user = users[question["user_id"]]
        gold_metadata = collection.get(ids=sorted(gold), include=["metadatas"])[
            "metadatas"
        ]
        if not all(is_visible(meta, user) for meta in gold_metadata):
            excluded += 1
            continue
        hits = dense_search(
            collection,
            client,
            question["question"],
            user,
            top_k=TOP_K,
            version=question["product_version"],
        )
        hit_ids = [hit["id"] for hit in hits]
        metric = calculate_metrics(hit_ids, gold, TOP_K)
        scores.append(metric)
        print(f"{question['id']} | Treffer={hit_ids[:3]} | Hit@5={metric['hit']:.0f}")

    if not scores:
        raise RuntimeError("Keine auswertbaren Fragen: Mapping und Index prüfen")

    print(f"\nBewertete Fragen: {len(scores)}; ausgeschlossen: {excluded}")

    for key in ("hit", "precision", "recall", "mrr"):
        print(f"{key:10s}: {sum(v[key] for v in scores) / len(scores):.3f}")

    print("Wichtig: Kein wissenschaftlich unabhängiger Blindtest.")


if __name__ == "__main__":
    main()
