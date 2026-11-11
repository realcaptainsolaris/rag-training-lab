"""
Station 03: Unsere erste Vektordatenbank mit Chroma

Lernziel:
Embeddings dauerhaft speichern und semantisch durchsuchen.

Index erstellen:
uv run python -m stations.03_chroma --index

Suche durchführen:
uv run python -m stations.03_chroma
"""

import argparse
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

CHROMA_DIR = Path("data/chroma_01")
COLLECTION_NAME = "rag_training"

QUESTION = "How long is an Orbit access token valid?"


parser = argparse.ArgumentParser()
parser.add_argument("--index", action="store_true")
args = parser.parse_args()

chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))


# 1. Dokumente
documents = [
    "Orbit retries failed webhook deliveries for 72 hours.",
    "Orbit access tokens are valid for 60 minutes.",
    "Orbit retains telemetry data for 90 days.",
    "Orbit limits API clients to 1000 requests per minute.",
    "Orbit exports telemetry data in CSV and JSON format.",
]

ids = ["chunk1", "chunk2", "chunk3", "chunk4", "chunk5"]


# 2. Index erstellen
if args.index:
    print("Erstelle Embeddings ...")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=documents,
    )

    vectors = [item.embedding for item in response.data]

    collection = chroma.get_or_create_collection(name=COLLECTION_NAME)

    # TODO:
    # Speichere IDs, Dokumente und Embeddings in Chroma.
    print("Gespeicherte Chunks:", collection.count())


# 3. Semantische Suche
else:
    collection = chroma.get_collection(name=COLLECTION_NAME)
    print("Gespeicherte Chunks:", collection.count())

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=QUESTION,
    )

    question_vector = response.data[0].embedding

    # TODO:
    # Suche die drei ähnlichsten Dokumente.
    #
    # Verwende question_vector und n_results=3.

    # results = collection.query(
    #     ...
    # )

    # print("\nFrage:", QUESTION)
    # print("\nGefundene Dokumente:")

    # for document, distance in zip(
    #     results["documents"][0],
    #     results["distances"][0],
    # ):
    #     print(f"{distance:.3f} | {document}")
