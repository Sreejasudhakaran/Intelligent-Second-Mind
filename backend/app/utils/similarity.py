from typing import List
import numpy as np


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def rank_by_similarity(
    query_embedding: List[float],
    candidates: List[dict],
    embedding_key: str = "embedding",
    top_k: int = 5,
) -> List[dict]:
    """
    Rank a list of candidate dicts by cosine similarity to a query embedding.
    Falls back to in-memory ranking when pgvector is unavailable.
    """
    scored = []
    for c in candidates:
        emb = c.get(embedding_key)
        if emb is None:
            continue
        score = cosine_similarity(query_embedding, emb)
        scored.append({**c, "similarity": round(score, 4)})

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
