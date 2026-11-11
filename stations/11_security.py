"""
Station 11: Zugriffskontrolle (ACL) bei RAG

Lernziel:
Eine Vektorsuche anhand von Benutzerrechten absichern.

Dokumente:
D003: PUBLIC
D008: CUSTOMER (org-amber)
D010: RESTRICTED

Index erstellen:
uv run python -m stations.11_security --index

Suche ausführen:
uv run python -m stations.11_security
"""

import argparse
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# 1. Konfiguration

PROJECT_DIR = Path(__file__).resolve().parent.parent

CORPUS_DIR = PROJECT_DIR / "data" / "teralune-mini" / "corpus"
CHROMA_DIR = PROJECT_DIR / "data" / "chroma_11"

COLLECTION_NAME = "teralune_acl"
EMBEDDING_MODEL = "text-embedding-3-small"

TOP_K = 3

DOCUMENTS = {
    "D003": {
        "access": "PUBLIC",
        "organization": "",
    },
    "D008": {
        "access": "CUSTOMER",
        "organization": "org-amber",
    },
    "D010": {
        "access": "RESTRICTED",
        "organization": "",
    },
}

USERS = {
    "anonymous": {
        "kind": "anonymous",
        "organization": "",
        "roles": [],
    },
    "customer_basic": {
        "kind": "customer",
        "organization": "org-amber",
        "roles": [],
    },
    "security_admin": {
        "kind": "internal",
        "organization": "",
        "roles": ["security_admin"],
    },
}


# Drei Fragen demonstrieren unterschiedliche Zugriffsrechte:
# D003 (PUBLIC):     Alle Benutzer dürfen das Dokument finden.
# D008 (CUSTOMER):   Nur customer_basic darf das Dokument finden.
# D010 (RESTRICTED): Nur security_admin darf das Dokument finden.
#
# Chroma kann trotzdem andere erlaubte Dokumente zurückgeben,
# auch wenn diese die Frage inhaltlich nicht beantworten.
QUESTIONS = [
    {
        "question": "How long does Orbit retry failed webhooks?",
        "expected": "D003",
    },
    {
        "question": "Why did measurements stop after the key rotation in TRAIN-208?",
        "expected": "D008",
    },
    {
        "question": "What is the marker for the current security exercise?",
        "expected": "D010",
    },
]

load_dotenv(PROJECT_DIR / ".env")


# 2. Dokumente indexieren


def index_documents(chroma, client):

    documents = []
    ids = []
    metadatas = []

    for doc_id, permissions in DOCUMENTS.items():
        matches = list(CORPUS_DIR.rglob(f"{doc_id}.md"))

        if len(matches) != 1:
            raise SystemExit(
                f"Erwartet genau eine Datei {doc_id}.md, gefunden: {len(matches)}"
            )

        path = matches[0]
        text = path.read_text(encoding="utf-8")

        ids.append(doc_id)
        documents.append(text)

        metadatas.append(
            {
                "source": path.name,
                "access": permissions["access"],
                "organization": permissions["organization"],
            }
        )

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=documents,
    )

    vectors = [item.embedding for item in response.data]

    try:
        chroma.delete_collection(name=COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        pass

    collection = chroma.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=vectors,
        metadatas=metadatas,
    )

    print("ACL-INDEX ERSTELLT")
    print("Dokumente:", collection.count())

    for doc_id, metadata in zip(ids, metadatas):
        print(f"  {doc_id}: {metadata['access']} ({metadata['organization']})")


def build_acl_filter(user):
    """
    Erstellt einen Chroma-Metadatenfilter für die Zugriffsrechte
    des Benutzers.

    PUBLIC ist immer erlaubt. Weitere Dokumente werden abhängig
    von Organisation und Benutzerrollen freigegeben.
    """
    allowed = [{"access": "PUBLIC"}]

    # TODO 1: CUSTOMER
    #
    # Wenn user["kind"] == "customer" ist,
    # ergänze einen Filter für CUSTOMER-Dokumente.
    #
    # Die Organisation muss mit
    # user["organization"] übereinstimmen.
    #
    # Verwende:
    # allowed.append(...)
    #
    # Kombiniere die beiden Bedingungen mit $and.

    # if ...:
    #     allowed.append(...)

    # TODO 2: RESTRICTED
    #
    # Wenn der Benutzer die Rolle security_admin
    # besitzt, darf er RESTRICTED-Dokumente sehen.
    #
    # Die Rollen stehen in user["roles"].
    #
    # Ergänze den entsprechenden Filter in allowed.

    # if ...:
    #     allowed.append(...)

    # Ein einzelner Filter benötigt kein $or.

    if len(allowed) == 1:
        return allowed[0]

    return {"$or": allowed}


# 4. Geschützte Vektorsuche


def search(collection, client, question, user, top_k=3):
    """
    Führt eine semantische Suche in Chroma durch.

    Der ACL-Filter beschränkt die Suche auf Dokumente,
    die der Benutzer lesen darf.
    """
    acl_filter = build_acl_filter(user)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question,
    )

    question_vector = response.data[0].embedding

    # TODO 3:
    # Ergänze den ACL-Filter bei collection.query().
    #
    # Verwende:
    # where=acl_filter
    #
    # Bis dahin liefert die Suche keine Treffer.
    # Dadurch werden keine geschützten Inhalte
    # versehentlich angezeigt.

    # results = collection.query(
    #     query_embeddings=[question_vector],
    #     n_results=top_k,
    #     where=...,
    #     include=["documents", "metadatas", "distances"],
    # )

    # hits = []
    #
    # for doc_id, metadata, distance in zip(
    #     results["ids"][0],
    #     results["metadatas"][0],
    #     results["distances"][0],
    # ):
    #     hits.append(
    #         {
    #             "id": doc_id,
    #             "access": metadata["access"],
    #             "distance": float(distance),
    #         }
    #     )
    #
    # return hits

    return []


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--index", action="store_true")
    args = parser.parse_args()

    client = OpenAI()

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if args.index:
        index_documents(chroma, client)
        return

    try:
        collection = chroma.get_collection(name=COLLECTION_NAME)
    except chromadb.errors.NotFoundError:
        raise SystemExit("ACL-Index fehlt. Zuerst Station 11 mit --index starten.")

    if collection.count() == 0:
        raise SystemExit("ACL-Index ist leer.")

    print("ACL-GESCHÜTZTE VEKTORSUCHE")
    print("Indexierte Dokumente:", collection.count())

    for user_id, user in USERS.items():
        print("\n" + "=" * 60)
        print("BENUTZER:", user_id)
        print("ACL-FILTER:", build_acl_filter(user))
        print("=" * 60)

        for item in QUESTIONS:
            question = item["question"]
            expected = item["expected"]

            hits = search(
                collection,
                client,
                question,
                user,
                top_k=TOP_K,
            )

            found_ids = [hit["id"] for hit in hits]

            print("\nFRAGE:", question)
            print("Gesuchtes Dokument:", expected)

            print("ERLAUBTE SUCHERGEBNISSE:")

            if not hits:
                print("  Keine Treffer")

            for hit in hits:
                print(f"  {hit['id']} ({hit['access']}) Distanz: {hit['distance']:.3f}")

            print(
                "Gesuchtes Dokument gefunden:",
                expected in found_ids,
            )


if __name__ == "__main__":
    main()
