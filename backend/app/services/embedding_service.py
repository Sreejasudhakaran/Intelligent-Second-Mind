from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from app.constants.categories import CATEGORIES

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Lazy-load the sentence-transformer model (384-dim)."""
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embedding(text: str) -> List[float]:
    """Generate a normalized 384-dim embedding vector."""
    model = get_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    model = get_model()
    return model.encode(texts, normalize_embeddings=True).tolist()


def classify_decision(title: str, reasoning: str = "") -> str:
    """
    Auto-classify a decision into a category using semantic cosine similarity
    against predefined category description strings.
    """
    model = get_model()
    input_text = f"{title} {reasoning}".strip()
    input_emb = model.encode(input_text, normalize_embeddings=True)

    best_category = "Strategy"
    best_score = -1.0

    for category, description in CATEGORIES.items():
        cat_emb = model.encode(description, normalize_embeddings=True)
        score = float(np.dot(input_emb, cat_emb))
        if score > best_score:
            best_score = score
            best_category = category

    return best_category
