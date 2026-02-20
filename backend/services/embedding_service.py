from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embedding(text: str) -> List[float]:
    """Generate a 384-dim embedding for the given text."""
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a batch of texts."""
    model = get_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return embeddings.tolist()


def classify_decision(title: str, reasoning: str) -> str:
    """Auto-classify a decision into a category using semantic similarity."""
    categories = {
        "Revenue Growth": "sales revenue growth business expansion monetization",
        "Maintenance": "maintenance fixing bugs technical debt infrastructure upkeep",
        "Brand": "branding marketing awareness content social media presence",
        "Admin": "administration meetings planning organization HR legal",
        "Strategy": "strategy vision long-term planning goals direction innovation",
    }

    input_text = f"{title} {reasoning}"
    model = get_model()
    input_emb = model.encode(input_text, normalize_embeddings=True)

    best_category = "Strategy"
    best_score = -1.0

    for category, description in categories.items():
        cat_emb = model.encode(description, normalize_embeddings=True)
        score = float(np.dot(input_emb, cat_emb))
        if score > best_score:
            best_score = score
            best_category = category

    return best_category
