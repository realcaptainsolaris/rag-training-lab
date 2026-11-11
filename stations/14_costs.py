"""
Station 14: Tokenverbrauch und echte API-Kosten

Lernziel:
Den Tokenverbrauch echter RAG-Anfragen messen
und daraus die API-Kosten berechnen.

Experiment:
Dieselbe Frage mit Top 1, Top 3 und Top 10 Chunks.

Start:
uv run python -m stations.14_costs
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
LLM_MODEL = "gpt-4.1-mini"

QUESTION = "How long is an Orbit 3 access token valid?"

TOP_K_VALUES = [1, 3, 10]
MONTHLY_REQUESTS = 10_000

# Beispielpreise in USD pro 1 Million Tokens.
EMBEDDING_PRICE = 0.02
LLM_INPUT_PRICE = 0.40
LLM_OUTPUT_PRICE = 1.60

INSTRUCTIONS = """
Answer the question using only the provided context.
If the context does not contain the answer, say that
you cannot determine the answer from the context.
Keep your answer short.
"""

load_dotenv(PROJECT_DIR / ".env")


# 2. Dense Retrieval


def embed_question(client, question):
    """Erzeugt das Frage-Embedding und liest dessen Tokenverbrauch."""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question,
    )

    return (
        response.data[0].embedding,
        response.usage.total_tokens,
    )


def dense_search(collection, vector, top_k=10):
    """Sucht die ähnlichsten Chunks in Chroma."""

    results = collection.query(
        query_embeddings=[vector],
        n_results=top_k,
        include=["documents"],
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


# 3. Kontext erstellen


def build_context(hits):
    """Erstellt einen Textkontext aus den gefundenen Chunks."""

    # TODO 1:
    # Erzeuge für jeden Treffer einen Textblock:
    #
    # Chunk-ID: D002_1
    # <Text des Chunks>
    #
    # Verbinde die Textblöcke mit "\n\n".
    #
    # Tipp: "\n\n".join(...)

    return ""


# 4. LLM aufrufen


def ask_llm(client, question, context):
    """Ruft das LLM auf und liefert Antwort und Tokenverbrauch."""

    prompt = f"""
Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model=LLM_MODEL,
        instructions=INSTRUCTIONS,
        input=prompt,
    )

    # TODO 2:
    # Lies die tatsächlichen Tokenzahlen aus:
    #
    # response.usage.input_tokens
    # response.usage.output_tokens
    #
    # Ersetze die beiden Nullen.

    return {
        "answer": response.output_text,
        "input_tokens": 0,
        "output_tokens": 0,
    }


# 5. Kosten berechnen


def calculate_cost(tokens, price_per_million):
    """Berechnet die Kosten aus Tokenzahl und Preis."""

    # TODO 3:
    # Berechne die Kosten.
    #
    # Der Preis gilt für 1 Million Tokens.

    return 0.0


# 6. Hauptprogramm


def main():

    client = OpenAI()

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        collection = chroma.get_collection(COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        raise SystemExit("Collection fehlt. Zuerst Station 05 indexieren.")

    if collection.count() == 0:
        raise SystemExit("Collection ist leer.")

    print("TOKENVERBRAUCH UND API-KOSTEN")
    print(f"Frage: {QUESTION}")

    vector, embedding_tokens = embed_question(
        client,
        QUESTION,
    )

    hits = dense_search(
        collection,
        vector,
        top_k=max(TOP_K_VALUES),
    )

    embedding_cost = calculate_cost(
        embedding_tokens,
        EMBEDDING_PRICE,
    )

    print(f"\nEmbedding-Tokens: {embedding_tokens}")
    print(f"Embedding-Kosten: ${embedding_cost:.8f}")

    measurements = []

    # Nach Bearbeitung der TODOs aktivieren:
    #
    # for top_k in TOP_K_VALUES:
    #
    #     selected_hits = hits[:top_k]
    #     context = build_context(selected_hits)
    #
    #     result = ask_llm(
    #         client,
    #         QUESTION,
    #         context,
    #     )
    #
    #     input_tokens = result["input_tokens"]
    #     output_tokens = result["output_tokens"]
    #
    #     input_cost = calculate_cost(
    #         input_tokens,
    #         LLM_INPUT_PRICE,
    #     )
    #
    #     output_cost = calculate_cost(
    #         output_tokens,
    #         LLM_OUTPUT_PRICE,
    #     )
    #
    #     request_cost = (
    #         embedding_cost
    #         + input_cost
    #         + output_cost
    #     )
    #
    #     measurements.append(
    #         {
    #             "top_k": top_k,
    #             "input_tokens": input_tokens,
    #             "output_tokens": output_tokens,
    #             "request_cost": request_cost,
    #         }
    #     )
    #
    #     print(f"\nEXPERIMENT TOP {top_k}")
    #     print("Antwort:", result["answer"])
    #     print("Input-Tokens:", input_tokens)
    #     print("Output-Tokens:", output_tokens)

    print("\nKOSTENVERGLEICH")
    print("=" * 70)

    print(
        f"{'Top K':<10}{'Input':>10}{'Output':>10}{'USD/Anfrage':>18}{'USD/Monat':>18}"
    )

    for measurement in measurements:
        monthly_cost = measurement["request_cost"] * MONTHLY_REQUESTS

        print(
            f"{measurement['top_k']:<10}"
            f"{measurement['input_tokens']:>10}"
            f"{measurement['output_tokens']:>10}"
            f"{measurement['request_cost']:>18.6f}"
            f"{monthly_cost:>18.2f}"
        )


if __name__ == "__main__":
    main()
