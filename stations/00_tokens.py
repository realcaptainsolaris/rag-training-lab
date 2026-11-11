"""
Station 00: Was sind Tokens?

Lernziel:
Verstehen, wie ein Sprachmodell Text in Tokens zerlegt.

Start:
uv run python -m stations.00_tokens
"""

import tiktoken

# 1. Text in Tokens zerlegen

text = "Hello, I am learning about RAG!"

encoding = tiktoken.get_encoding("cl100k_base")
tokens = encoding.encode(text)

print("Text:", text)
print("Token-IDs:", tokens)


# 2. Einzelne Tokens sichtbar machen
print("Einzelne Tokens:")
# TODO:
# Durchlaufe alle Token-IDs mit einer for-Schleife.
# Gib für jedes Token die ID und den dekodierten Text aus.


# 3. Wörter und Tokens vergleichen

text = "Retrieval-Augmented Generation ist spannend!"

# TODO:
# 1. Tokenisiere den neuen Text.
# 2. Gib die Anzahl der Wörter aus.
# 3. Gib die Anzahl der Tokens aus.
#
# Tipps:
# text.split()
# len()


# 4. Eigenes Experiment

# TODO:
# Probiere verschiedene Texte aus.
#
# "Hallo Welt!"
# "Hello World!"
# "Donaudampfschifffahrtsgesellschaft"
#
# Unterscheiden sich Wortanzahl und Tokenanzahl?
