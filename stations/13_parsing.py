"""
Station 13: HTML und CSV parsen

Lernziel:
HTML-Dateien und CSV-Tabellen in Text umwandeln.

HTML:
    Text aus HTML-Elementen extrahieren.

CSV:
    Jede Tabellenzeile als eigenen Textblock darstellen.

Start:
uv run python -m stations.13_parsing
"""

import csv
from html.parser import HTMLParser
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "teralune-mini" / "corpus" / "public"


class TextExtractor(HTMLParser):
    """Sammelt Textabschnitte aus einem HTML-Dokument."""

    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        # TODO 1:
        # Entferne führende und abschließende Leerzeichen.
        #
        # Füge den Text zu self.parts hinzu,
        # wenn er nicht leer ist.
        #
        # Tipp: data.strip()

        pass


def parse_html(path):
    """Liest HTML und gibt den extrahierten Text zurück."""

    parser = TextExtractor()

    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()

    return "\n".join(parser.parts)


def parse_csv(path):
    """
    Wandelt jede CSV-Zeile in einen Textblock um.

    Spaltennamen und Werte sollen gemeinsam
    im Text stehen.
    """

    documents = []

    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # TODO 2:
            # Wandle jede Tabellenzeile in Text um.
            #
            # Beispiel:
            #
            # plan: Team
            # devices_per_organization: 1000
            #
            # Tipp:
            # row.items() liefert Spaltenname und Wert.
            #
            # Verbinde die Felder mit "\n".
            # Füge den Text zu documents hinzu.

            pass

    return documents


def main():

    html_file = DATA_DIR / "D006.html"
    html_text = parse_html(html_file)

    print("HTML: D006.html")
    print("=" * 55)
    print(html_text)

    csv_file = DATA_DIR / "D007.csv"
    csv_documents = parse_csv(csv_file)

    print("\nCSV: D007.csv")
    print("=" * 55)

    for number, text in enumerate(csv_documents, start=1):
        print(f"\nDatensatz {number}")
        print(text)

    print(f"\nErzeugte CSV-Textblöcke: {len(csv_documents)}")


if __name__ == "__main__":
    main()
