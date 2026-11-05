"""Station 2: Fixed Size, Overlap und Struktur-Chunking vergleichen.

Start: uv run python -m stations.02_chunking
Experiment: CHUNK_SIZE oder OVERLAP ändern.
"""

import tiktoken

from training_rag.documents import DATA_DIR, structure_chunks

FILE = DATA_DIR / "corpus" / "public" / "D022.md"
CHUNK_SIZE = 150
OVERLAP = 30


def fixed_chunks(tokens: list[int], size: int, step: int, encoding) -> list[str]:
    return [encoding.decode(tokens[start:start + size])
            for start in range(0, len(tokens), step)]


def main() -> None:
    text = FILE.read_text(encoding="utf-8")
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    strategies = {
        "Fixed Size": fixed_chunks(tokens, CHUNK_SIZE, CHUNK_SIZE, encoding),
        "Mit Overlap": fixed_chunks(tokens, CHUNK_SIZE, CHUNK_SIZE - OVERLAP, encoding),
        "Strukturorientiert": [f"{path}\n{part}" for path, part in structure_chunks(text)],
    }
    print(f"Dokument: {FILE.name} ({len(tokens)} Tokens)")
    for strategy, parts in strategies.items():
        print(f"\n{strategy}: {len(parts)} Chunks")
        for i, part in enumerate(parts[:2], 1):
            print(f"  Chunk {i}: {part[:130].replace(chr(10), ' ')} ...")
    print("\nBeobachtung: Welche Strategie erhält die Cursor-Überschrift?")
    print("Die tatsächliche Retrieval-Qualität messen wir in der nächsten Station.")


if __name__ == "__main__":
    main()
