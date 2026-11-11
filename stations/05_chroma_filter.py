"""
Station 05: Metadaten und Versionsfilter in Chroma

Lernziel:
Metadaten speichern und die semantische Suche
auf bestimmte Produktversionen beschränken.

Index erstellen:
uv run python -m stations.05_chroma_filter --index

Suche durchführen:
uv run python -m stations.05_chroma_filter
"""

import argparse
import json
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = PROJECT_DIR / "data" / "teralune-mini"
MANIFEST_FILE = CORPUS_DIR / "manifest.json"
CHROMA_DIR = PROJECT_DIR / "data" / "chroma_05"

COLLECTION_NAME = "teralune_metadata"
QUESTION = "How long is an Orbit 3 access token valid?"
FILTER_VERSION = "3.0"

load_dotenv(PROJECT_DIR / ".env")
client = OpenAI()
chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))


def structure_chunks(text):
    """Zerlegt Markdown-Text anhand seiner Überschriften."""

    chunks = []
    current_chunk = ""

    for line in text.splitlines():
        if line.startswith(("# ", "## ", "### ")):
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# 1. Index mit Metadaten aufbauen


def build_index():

    manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))

    documents = []
    ids = []
    metadatas = []

    for entry in manifest:
        if entry["access"] != "PUBLIC":
            continue

        if entry["format"] != "md":
            continue

        file = CORPUS_DIR / entry["path"]
        text = file.read_text(encoding="utf-8")
        chunks = structure_chunks(text)

        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            ids.append(f"{entry['id']}_{i}")

            # TODO 1:
            # Ergänze für jeden Chunk ein Dictionary mit:
            # source, version und status.
            #
            # Die Werte stehen in entry und file.name.

            # metadatas.append(
            #     {
            #         ...
            #     }
            # )

    print("Erzeugte Chunks:", len(documents))

    if not documents:
        raise SystemExit("Keine Dokumente gefunden.")

    # Embeddings erzeugen

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=documents,
    )

    vectors = [item.embedding for item in response.data]

    print("Erzeugte Embeddings:", len(vectors))

    # Collection neu erstellen

    try:
        chroma.delete_collection(name=COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        pass

    collection = chroma.create_collection(name=COLLECTION_NAME)

    # TODO 2:
    # Ergänze metadatas=metadatas beim Speichern.
    #
    # Wichtig: TODO 1 muss vorher erledigt sein.

    # collection.upsert(
    #     ids=ids,
    #     documents=documents,
    #     embeddings=vectors,
    #     metadatas=metadatas,
    # )

    print("Gespeicherte Chunks:", collection.count())


# 2. Programm starten

parser = argparse.ArgumentParser()
parser.add_argument("--index", action="store_true")
args = parser.parse_args()

if args.index:
    build_index()

else:
    try:
        collection = chroma.get_collection(name=COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        raise SystemExit("Collection fehlt. Zuerst mit --index indexieren.")

    if collection.count() == 0:
        raise SystemExit("Collection ist leer. Zuerst TODO 1 und 2 bearbeiten.")

    print("Gespeicherte Chunks:", collection.count())

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=QUESTION,
    )

    question_vector = response.data[0].embedding

    # 3. Suche ohne Filter

    results = collection.query(
        query_embeddings=[question_vector],
        n_results=3,
    )

    print("\nSUCHE OHNE FILTER")

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        print(f"\n{metadata['source']} | Version {metadata['version']}")
        print(f"Distanz: {distance:.3f}")
        print(document[:400])

    # 4. Suche mit Versionsfilter

    # TODO 3:
    # Ergänze einen Filter, der ausschließlich
    # Dokumente der Version FILTER_VERSION berücksichtigt.
    #
    # Tipp: where={"version": ...}

    # filtered_results = collection.query(
    #     query_embeddings=[question_vector],
    #     n_results=3,
    # )

    # print("\nSUCHE MIT FILTER:", FILTER_VERSION)

    # for document, metadata, distance in zip(
    #     filtered_results["documents"][0],
    #     filtered_results["metadatas"][0],
    #     filtered_results["distances"][0],
    # ):
    #     print(f"\n{metadata['source']} | Version {metadata['version']}")
    #     print(f"Distanz: {distance:.3f}")
    #     print(document[:400])


# 5. Experiment

# Verändere FILTER_VERSION zwischen "2.4" und "3.0".
# Vergleiche die gefundenen Dokumente.
