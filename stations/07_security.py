"""Station 7: Zugriffskontrolle muss VOR dem Retrieval gelten.

Diese Demonstration benötigt KEINEN OpenAI-Schlüssel.
Start: uv run python -m stations.07_security
"""

from training_rag.documents import load_chunks
from training_rag.pipeline import is_visible, load_users

USERS = ["anonymous", "customer_basic", "customer_cobalt", "teralune_engineer", "security_admin"]
DOCS = ["D003", "D008", "D009", "D010", "D037"]


def main() -> None:
    chunks = load_chunks()
    metadata = {chunk.document_id: chunk.metadata for chunk in chunks}
    users = load_users()
    print("Zulässige Dokumente nach Zugriffsklasse und Organisation")
    print(f"{'Benutzer':22s} " + " ".join(f"{doc:>5}" for doc in DOCS))
    for user_id in USERS:
        user = users[user_id]
        visible = ["JA" if is_visible(metadata[doc_id], user) else "NEIN"
                   for doc_id in DOCS]
        print(f"{user_id:22s} " + " ".join(f"{value:>5}" for value in visible))
    print("\nFür echte Anwendungen Rechte serverseitig durchsetzen, nicht bloß im Prompt.")
    print("Dokumentanweisungen (z. B. in D011) sind keine Systemanweisungen.")


if __name__ == "__main__":
    main()
