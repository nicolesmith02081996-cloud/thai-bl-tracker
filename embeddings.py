from sentence_transformers import SentenceTransformer
import numpy as np
import json

# lightweight model (fast + good enough)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):

    vector = model.encode(text)

    return json.dumps(vector.tolist())


def cosine_similarity(vec1, vec2):

    a = np.array(json.loads(vec1))
    b = np.array(json.loads(vec2))

    return float(
        np.dot(a, b) /
        (np.linalg.norm(a) * np.linalg.norm(b))
    )