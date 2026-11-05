from training_rag.pipeline import get_collection

collection = get_collection()

result = collection.get(
    ids=["D033-chunk-1"],
    include=["documents", "metadatas", "embeddings"],
)

print("Collection:", collection.name)
print("Gespeicherte Einträge:", collection.count())
print("Chunk-ID:", result["ids"][0])
print("Text:", result["documents"][0])
print("Metadaten:", result["metadatas"][0])
print("Embedding-Dimensionen:", len(result["embeddings"][0]))
print("Embedding (erste 5 Werte):", result["embeddings"][0][:5])
