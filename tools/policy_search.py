
import json
import re
from pathlib import Path

import faiss
import numpy as np
from crewai.tools import tool

from config.settings import POLICY_TOP_K


BASE_DIR = Path(__file__).resolve().parents[1]
POLICY_DIR = BASE_DIR / "policy"
POLICIES_FILE = POLICY_DIR / "policies.json"
INDEX_FILE = POLICY_DIR / "policy.index"
METADATA_FILE = POLICY_DIR / "metadata.json"


def _tokens(text: str):
    return re.findall(r"[a-z0-9]+", text.lower())


def _vectorize(text: str, dimension: int = 384) -> np.ndarray:
    """Small deterministic hashing vectorizer; avoids an extra embedding framework."""
    vector = np.zeros(dimension, dtype=np.float32)
    tokens = _tokens(text)

    for token in tokens:
        vector[hash(token) % dimension] += 1.0

    for left, right in zip(tokens, tokens[1:]):
        vector[hash(left + "_" + right) % dimension] += 0.5

    norm = np.linalg.norm(vector)
    if norm:
        vector /= norm

    return vector


def _load_policy_records():
    with open(POLICIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _build_index():
    records = _load_policy_records()
    vectors = np.vstack([
        _vectorize(
            f"{r['program']} {r['policy_id']} {r['title']} "
            f"{r['requirement']} {r.get('exceptions', '')} {r.get('keywords', '')}"
        )
        for r in records
    ]).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    metadata = {
        "dimension": vectors.shape[1],
        "records": records,
    }

    faiss.write_index(index, str(INDEX_FILE))
    with open(METADATA_FILE, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    return index, metadata


def _load_index():
    try:
        index = faiss.read_index(str(INDEX_FILE))
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        if index.ntotal != len(metadata["records"]):
            raise ValueError("Index and metadata record counts differ.")

        return index, metadata
    except Exception:
        return _build_index()


def search_policies(query: str, top_k: int = POLICY_TOP_K) -> list[dict]:
    index, metadata = _load_index()
    vector = _vectorize(query).reshape(1, -1)
    scores, positions = index.search(vector, min(top_k, index.ntotal))

    results = []
    for score, position in zip(scores[0], positions[0]):
        if position < 0:
            continue
        record = dict(metadata["records"][int(position)])
        record["similarity"] = round(float(score), 4)
        results.append(record)

    return results


@tool("search_mortgage_policy")
def policy_search_tool(query: str, top_k: int = POLICY_TOP_K) -> str:
    """Search the local FAISS mortgage policy library and return cited policy records."""
    results = search_policies(query, top_k)
    if not results:
        return "INSUFFICIENT POLICY EVIDENCE"

    return json.dumps(results, indent=2)
