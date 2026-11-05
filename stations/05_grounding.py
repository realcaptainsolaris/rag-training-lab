"""Station 5: Grounding und Quellenbezug mit echtem Retrieval-Kontext.

Vorher Chroma-Index aufbauen. Teste eine nicht beantwortbare Frage.
Start: uv run python -m stations.05_grounding
"""

from training_rag.pipeline import (
    answer,
    build_context,
    dense_search,
    get_client,
    get_collection,
    load_users,
)

QUESTIONS = [
    "Wie lange versucht Orbit 3.0 fehlgeschlagene Webhooks erneut?",
    "Welche offiziellen Rabatte bekommen Universitäten?",
]


def main() -> None:
    client = get_client()
    collection = get_collection()
    user = load_users()["anonymous"]
    for question in QUESTIONS:
        hits = dense_search(
            collection,
            client,
            question,
            user,
            top_k=3,
            version="3.0",
            current_only=True,
        )
        context = build_context(hits)
        print("\nFrage:", question)
        print("Quellen im Kontext:", [hit["metadata"]["document_id"] for hit in hits])
        print("Antwort:", answer(client, question, context))
        print("Achtung: Ein Prompt garantiert keine Faktentreue. Quellen prüfen!")


if __name__ == "__main__":
    main()
