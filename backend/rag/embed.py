from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List

# -------------------- GLOBALS (LAZY INIT) --------------------

_model = None
_index = None
_documents: List[str] = []

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


# -------------------- LOADERS --------------------

def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _load_index():
    global _index
    if _index is None:
        # cosine similarity using normalized vectors
        _index = faiss.IndexFlatIP(EMBEDDING_DIM)
    return _index


# -------------------- CORE API --------------------

def embed_texts(texts, tag: str = "GENERAL"):
    """
    Embed text(s) and store in FAISS.
    """
    if isinstance(texts, str):
        texts = [texts]

    tagged_texts = [f"[{tag}] {t}" for t in texts]
    model = _load_model()
    index = _load_index()
    embeddings = model.encode(tagged_texts)
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    _documents.extend(tagged_texts)
    return embeddings


# -------------------- SEMANTIC SEARCH --------------------

def search(query: str, top_k: int = 3):
    """
    Retrieve most relevant stored documents.

    Args:
        query (str)
        top_k (int)

    Returns:
        list of retrieved texts
    """

    model = _load_model()
    index = _load_index()

    if index.ntotal == 0:
        return []

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for i in indices[0]:
        if 0 <= i < len(_documents):
            results.append(_documents[i])

    return results


# -------------------- ACCESSORS --------------------

def get_faiss_index():
    return _load_index()


def get_documents():
    return _documents


# -------------------- RESET (useful for demo) --------------------

def reset_index():
    global _index, _documents
    _index = None
    _documents = []