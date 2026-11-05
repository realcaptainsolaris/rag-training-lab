"""Station 1: Erste vollständige RAG-Pipeline mit fünf Texten aus dem Buch.

Start: uv run python -m stations.01_first_rag
Experiment: QUESTION ändern und das Ergebnis beobachten.
"""

from training_rag.pipeline import answer, embed, get_client

DOCUMENTS = [
    "Orbit retries failed webhook deliveries for 72 hours.",
    "Orbit access tokens are valid for 60 minutes.",
    "Orbit retains telemetry data for 90 days.",
    "Orbit limits API clients to 1000 requests per minute.",
    "Orbit exports telemetry data in CSV and JSON format.",
]
QUESTION = "How long does Orbit retry a failed webhook delivery?"


def cosine(a: list[float], b: list[float]) -> float:
    """Kosinusähnlichkeit als Skalarprodukt normierter Vektoren."""
    from math import sqrt

    ab = sum(x * y for x, y in zip(a, b))
    return ab / (sqrt(sum(x * x for x in a)) * sqrt(sum(y * y for y in b)))


def main() -> None:
    client = get_client()
    embeddings = embed(client, DOCUMENTS + [QUESTION])
    question_vector = embeddings[-1]
    ranked = sorted(
        zip(DOCUMENTS, [cosine(question_vector, v) for v in embeddings[:-1]]),
        key=lambda item: item[1], reverse=True,
    )
    print("Frage:", QUESTION)
    print("\nRetrieval (Score ist KEINE Wahrscheinlichkeit):")
    for doc, score in ranked[:3]:
        print(f"  {score:.4f} | {doc}")
    context = "\n".join(doc for doc, _ in ranked[:2])
    print("\nAntwort:")
    print(answer(client, QUESTION, context))


if __name__ == "__main__":
    main()
