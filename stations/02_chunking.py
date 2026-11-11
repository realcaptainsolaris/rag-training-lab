"""
Station 02: Dokumente in Chunks zerlegen

Lernziel:
Drei Chunking-Strategien kennenlernen:
1. Fixed Size
2. Overlap
3. Structure Chunking

Start:
uv run python -m stations.02_chunking
"""

from pathlib import Path

# 1. Dokument laden
PROJECT_DIR = Path(__file__).resolve().parent.parent
FILE = PROJECT_DIR / "data" / "teralune-mini" / "corpus" / "public" / "D022.md"

text = FILE.read_text(encoding="utf-8")
print("Dokument:", FILE.name)
print("Anzahl Zeichen:", len(text))


# 2. Fixed Size Chunking
CHUNK_SIZE = 500

chunks = []

for start in range(0, len(text), CHUNK_SIZE):
    chunk = text[start : start + CHUNK_SIZE]
    chunks.append(chunk)

print("\nFIXED SIZE")
print("Anzahl Chunks:", len(chunks))
print("Erster Chunk:\n", chunks[0])


# 3. Chunking mit Overlap

OVERLAP = 100

# TODO:
# Erzeuge Chunks mit jeweils 100 Zeichen Überlappung.
#
# step = CHUNK_SIZE - OVERLAP
# overlap_chunks = []

# print("\nMIT OVERLAP")
# print("Anzahl Chunks:", len(overlap_chunks))
# print("Erster Chunk:\n", overlap_chunks[0])
# print("Zweiter Chunk:\n", overlap_chunks[1])


# 4. Structure Chunking (simplified)

# TODO:
# Zerlege den Text anhand seiner Markdown-Überschriften.
#
# Eine neue Überschrift beginnt einen neuen Chunk.
# Erkenne Überschriften mit #, ## und ###.
#
# line.startswith(("# ", "## ", "### "))

# structure_chunks = []
# current_chunk = ""

# print("\nSTRUCTURE CHUNKING")
# print("Anzahl Chunks:", len(structure_chunks))
# print("Erster Chunk:\n", structure_chunks[0])


# 5. Vergleich

# TODO:
# Vergleiche die Anzahl der Chunks aller drei Strategien.


# 6. Experiment

# Verändere CHUNK_SIZE und OVERLAP.
# Wie verändert sich die Anzahl der Chunks?
