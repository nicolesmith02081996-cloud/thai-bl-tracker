from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine
import traceback

# ==========================================
# LOAD MODEL ONCE
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

print("🧠 Loading embedding model...")

try:
    model = SentenceTransformer(MODEL_NAME)
    print("✅ Embedding model loaded")

except Exception as e:
    print("❌ Failed to load embedding model:", e)
    traceback.print_exc()
    model = None


# ==========================================
# CLEAN INPUT TEXT
# ==========================================

def prepare_text(event):

    if isinstance(event, dict):

        text = " ".join([
            str(event.get("company", "")),
            str(event.get("actors", "")),
            str(event.get("date", "")),
            str(event.get("location", "")),
            str(event.get("summary", ""))
        ])

        return text.strip()

    return str(event).strip()


# ==========================================
# GENERATE EMBEDDING
# ==========================================

def get_embedding(event):

    if model is None:
        return None

    try:

        text = prepare_text(event)

        if not text:
            return None

        embedding = model.encode(
            text,
            convert_to_tensor=False
        )

        # PostgreSQL-friendly storage
        return embedding.tolist()

    except Exception as e:

        print("❌ Embedding error:", e)

        return None


# ==========================================
# COSINE SIMILARITY
# ==========================================

def cosine_similarity(vec1, vec2):

    try:

        if not vec1 or not vec2:
            return 0

        score = sklearn_cosine(
            [vec1],
            [vec2]
        )[0][0]

        return float(score)

    except Exception:

        return 0


# ==========================================
# DUPLICATE CHECK HELPER
# ==========================================

def are_duplicates(
        embedding1,
        embedding2,
        threshold=0.85):

    score = cosine_similarity(
        embedding1,
        embedding2
    )

    return score >= threshold


# ==========================================
# LOCAL TEST
# ==========================================

if __name__ == "__main__":

    event1 = {
        "company": "GMMTV",
        "actors": ["Gemini", "Fourth"],
        "date": "2027-04-10",
        "location": "Bangkok",
        "summary": "GeminiFourth fan meeting in Bangkok."
    }

    event2 = {
        "company": "GMMTV",
        "actors": ["Gemini", "Fourth"],
        "date": "2027-04-10",
        "location": "Bangkok",
        "summary": "Official Gemini and Fourth fan meeting."
    }

    emb1 = get_embedding(event1)
    emb2 = get_embedding(event2)

    score = cosine_similarity(emb1, emb2)

    print("Similarity Score:", score)

    if are_duplicates(emb1, emb2):
        print("⚠️ Duplicate detected")
    else:
        print("✅ Unique event")