"""Retrieval-Metriken aus Buchkapitel 6, ohne externe Bibliotheken."""


def calculate_metrics(retrieved: list[str], gold: set[str], top_k: int = 5) -> dict[str, float]:
    """Metriken gelten nur für beantwortbare Fragen mit positivem Goldset."""
    if not gold:
        raise ValueError("Goldset darf nicht leer sein")
    retrieved = retrieved[:top_k]
    hits = [cid in gold for cid in retrieved]
    return {
        "hit": float(any(hits)),
        "precision": sum(hits) / top_k,
        "recall": sum(hits) / len(gold),
        "mrr": next((1 / i for i, hit in enumerate(hits, 1) if hit), 0.0),
    }
