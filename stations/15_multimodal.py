"""
Station 15: Multimodales RAG mit Bildern

Lernziel:
Bilder mit einem Vision-Modell beschreiben und
anschließend über Text-Embeddings suchen.

Start:
uv run python -m stations.15_multimodal --index
uv run python -m stations.15_multimodal
"""

import argparse
import base64
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# 1. Konfiguration

PROJECT_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = PROJECT_DIR / "data" / "images"
CHROMA_DIR = PROJECT_DIR / "data" / "chroma_15"

COLLECTION_NAME = "orbit_images"

VISION_MODEL = "gpt-4.1-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

IMAGES = [
    "Technische_Übersicht_orbit_API-Plattform-1.png",
    "OrbitAPI_ HTTP-403-Fehlerbehebung-2.png",
    "OrbitAPI_Monitoring_Dashboard-3.png",
]

QUESTIONS = [
    "Which image explains the architecture of the Orbit API?",
    "Which image shows a missing API permission?",
    "Which image shows increased latency after a deployment?",
]

load_dotenv(PROJECT_DIR / ".env")


# 2. Bilder beschreiben


def describe_image(client, path):
    """Erzeugt eine durchsuchbare Beschreibung eines Bildes."""

    image_bytes = path.read_bytes()
    encoded_image = base64.b64encode(image_bytes).decode("ascii")

    image_url = f"data:image/png;base64,{encoded_image}"

    # TODO 1:
    # Rufe die Responses API mit VISION_MODEL auf.
    #
    # Übergebe zwei Content-Elemente:
    #
    # 1. input_text:
    #    Bitte um eine englische Beschreibung des Bildes.
    #
    # 2. input_image:
    #    Verwende image_url.
    #
    # Gib response.output_text zurück.

    return ""


# 3. Text-Embeddings


def embed_text(client, text):
    """Erzeugt ein Embedding für einen Text."""

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


# 4. Bilder indexieren


def index_images(chroma, client):
    """Speichert Bildbeschreibungen und Embeddings in Chroma."""

    for filename in IMAGES:
        if not (IMAGE_DIR / filename).is_file():
            raise SystemExit(f"Bild fehlt: {filename}")

    try:
        chroma.delete_collection(COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        pass

    collection = chroma.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    for number, filename in enumerate(IMAGES, start=1):
        path = IMAGE_DIR / filename

        print(f"\nBILD {number}: {filename}")

        description = describe_image(client, path)

        if not description:
            print("Keine Beschreibung vorhanden.")
            continue

        print("\nBildbeschreibung:")
        print(description)

        vector = embed_text(client, description)

        # TODO 2:
        # Speichere den Datensatz mit collection.add().
        #
        # ID:         f"IMG_{number:03}"
        # Dokument:   description
        # Embedding:  vector
        # Metadaten:  {"filename": filename}
        #
        # Übergib die Werte jeweils als Liste.

    print(f"\nIndexiert: {collection.count()} Bilder")


# 5. Bilder suchen


def search_image(collection, client, question):
    """Sucht das passende Bild anhand seiner Beschreibung."""

    question_vector = embed_text(client, question)

    # TODO 3:
    # Suche mit collection.query() nach dem ähnlichsten
    # Bildbeschreibung-Vektor.
    #
    # Verwende:
    # query_embeddings=[question_vector]
    # n_results=1
    #
    # Fordere documents, metadatas und distances an.
    #
    # Gib ID, Beschreibung, Dateiname und Distanz zurück.


# 6. Hauptprogramm


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--index", action="store_true")
    args = parser.parse_args()

    client = OpenAI()

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if args.index:
        index_images(chroma, client)
        return

    try:
        collection = chroma.get_collection(COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        raise SystemExit("Bildindex fehlt. Zuerst mit --index starten.")

    if collection.count() == 0:
        print("Bildindex ist leer. TODO 1 und 2 bearbeiten.")
        return

    for question in QUESTIONS:
        print(f"\nFRAGE: {question}")

        hit = search_image(
            collection,
            client,
            question,
        )

        if hit is None:
            print("TODO 3 noch nicht implementiert.")
            continue

        print(f"Treffer:  {hit['filename']}")
        print(f"Distanz:  {hit['distance']:.3f}")
        print(f"Bildpfad: {IMAGE_DIR / hit['filename']}")

        print("\nGespeicherte Bildbeschreibung:")
        print(hit["description"])


if __name__ == "__main__":
    main()
