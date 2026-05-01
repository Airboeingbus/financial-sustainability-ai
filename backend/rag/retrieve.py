import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rag.embed import get_faiss_index, get_documents

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


# -------------------- LOAD MODEL --------------------

def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


# -------------------- RETRIEVE CONTEXT --------------------

def retrieve_context(query: str, k: int = 3):
    """
    Retrieve top-k relevant document chunks for a query.

    Args:
        query (str): user query
        k (int): number of results

    Returns:
        dict with retrieved texts and combined context
    """

    index = get_faiss_index()
    documents = get_documents()

    if index.ntotal == 0:
        return {
            "context": "",
            "documents": [],
            "message": "No indexed report context available."
        }

    model = _load_model()

    # embed query
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # normalize for cosine similarity
    faiss.normalize_L2(query_embedding)

    k = min(k, len(documents))

    scores, indices = index.search(query_embedding, k)

    results = []

    for idx in indices[0]:
        if 0 <= idx < len(documents):
            results.append(documents[idx])

    combined_context = "\n".join(results)

    return {
        "context": combined_context,
        "documents": results,
        "scores": scores[0].tolist()
    }