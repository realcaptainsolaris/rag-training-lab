"""Laden, Parsen und Struktur-Chunking nach den Beispielen aus Buchkapitel 2."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "teralune-mini"


@dataclass(frozen=True)
class Chunk:
    """Text-Chunk einschließlich Quellen- und Zugriffsmetadaten."""

    chunk_id: str
    document_id: str
    text: str
    headings: str
    source: str
    metadata: dict[str, str]

    @property
    def embedding_text(self) -> str:
        """Wie im Buch: Überschriften erhöhen den Kontext des Embeddings."""
        return f"{self.headings}\n\n{self.text}" if self.headings else self.text


def load_manifest() -> list[dict]:
    """Lädt ausschließlich die im Seminar enthaltenen 16 Dokumente."""
    return json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))


def parse_document(path: Path) -> str:
    """Einheitlicher Text aus Markdown, HTML oder CSV."""
    if path.suffix == ".md":
        return path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        return soup.get_text("\n", strip=True)
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as handle:
            return "\n".join(" | ".join(row) for row in csv.reader(handle))
    raise ValueError(f"Nicht unterstütztes Format: {path.suffix}")


def structure_chunks(text: str) -> list[tuple[str, str]]:
    """Markdown nach Überschriften splitten, analog zum Buchcode.

    Nur echte Überschriften (# mit folgendem Leerzeichen) beginnen Chunks.
    In Codeblöcken wird nicht auf Überschriften geprüft.
    """
    result: list[tuple[str, str]] = []
    headings: dict[int, str] = {}
    current_level: int | None = None
    current_lines: list[str] = []
    in_fence = False

    def flush() -> None:
        content = "\n".join(current_lines).strip()
        if current_level is not None and content:
            result.append((" > ".join(headings[level] for level in sorted(headings)), content))

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if level <= 6 and line[level:level + 1] == " ":
                flush()
                headings[level] = line[level:].strip()
                for deeper in list(headings):
                    if deeper > level:
                        del headings[deeper]
                current_level = level
                current_lines = []
                continue
        current_lines.append(line)
    flush()
    return result


def load_chunks() -> list[Chunk]:
    """Erzeugt stabile IDs Dxxx-chunk-n und fügt Manifest-Metadaten hinzu."""
    chunks: list[Chunk] = []
    for doc in load_manifest():
        path = DATA_DIR / doc["path"]
        text = parse_document(path)
        pieces = structure_chunks(text) if path.suffix == ".md" else [(doc["title"], text)]
        metadata = {
            "document_id": doc["id"],
            "version": doc["version"],
            "status": doc["status"],
            "access": doc["access"],
            "organization": doc.get("organization") or "",
            "required_roles": ",".join(doc.get("required_roles") or []),
            "source": doc["path"],
        }
        for number, (headings, content) in enumerate(pieces, start=1):
            chunks.append(Chunk(
                chunk_id=f"{doc['id']}-chunk-{number}",
                document_id=doc["id"],
                text=content,
                headings=headings,
                source=doc["path"],
                metadata={**metadata, "headings": headings, "chunk_number": str(number)},
            ))
    return chunks
