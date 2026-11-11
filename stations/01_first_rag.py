"""
Station 01: Unsere erste RAG-Pipeline

Lernziel:
Dokumente mit Embeddings durchsuchen und eine Frage
mithilfe eines Sprachmodells beantworten.

Start:
uv run python -m stations.01_first_rag
"""

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


documents = [
    "Orbit retries failed webhook deliveries for 72 hours.",
    "Orbit access tokens are valid for 60 minutes.",
    "Orbit retains telemetry data for 90 days.",
    "Orbit limits API clients to 1000 requests per minute.",
    "Orbit exports telemetry data in CSV and JSON format.",
]

question = "How long does Orbit retry a failed webhook delivery?"

print("Frage:", question)

# 1. Embeddings erzeugen

# TODO: Embeddings für Dokumente und Frage erzeugen.
# Modell: text-embedding-3-small

# Nach diesem Schritt:
# print("Anzahl Vektoren:", len(vectors))
# print("Dimensionen:", len(vectors[0]))


# 2. Ähnlichkeit berechnen

# TODO: Cosine Similarity zwischen Frage und Dokumenten berechnen.
# Bei normierten Embeddings genügt das Skalarprodukt.

# similarities = document_vectors @ question_vector


# 3. Retrieval

# TODO Das Dokument mit der höchsten Ähnlichkeit auswählen.

# best_index = ...
# best_document = documents[best_index]


# 4. Antwort generieren

# TODO: Frage und gefundenes Dokument an gpt-4.1-mini übergeben.

# print(response.output_text)
