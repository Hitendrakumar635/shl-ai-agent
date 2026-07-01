from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from services.catalog import load_catalog

# ----------------------------
# Load model & catalog
# ----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

catalog = load_catalog()

documents = []

for item in catalog:

    text = " ".join([
        item.get("name", ""),
        item.get("description", ""),
        " ".join(item.get("job_levels", [])),
        " ".join(item.get("keys", []))
    ])

    documents.append(text.lower())

embeddings = model.encode(documents)


# ----------------------------
# Query Expansion
# ----------------------------

def expand_query(query):

    q = query.lower()

    extra = []

    mapping = {
        "java": ["java", "developer", "backend"],
        "python": ["python", "developer", "programming"],
        "sales": ["sales", "customer", "selling"],
        "manager": ["manager", "leadership"],
        "leadership": ["manager", "leadership"],
        "graduate": ["entry", "graduate"],
        "personality": ["opq", "behavior", "personality"],
        "behavior": ["opq", "behavior"],
        "coding": ["developer", "programming"],
        "developer": ["software", "programming"],
        "customer": ["customer service"],
        "service": ["customer service"],
        "finance": ["financial"],
        "analyst": ["analysis"],
        "engineer": ["engineering"]
    }

    for key, value in mapping.items():

        if key in q:
            extra.extend(value)

    return query + " " + " ".join(extra)


# ----------------------------
# Search
# ----------------------------

def search_assessments(query, top_k=10):

    expanded = expand_query(query)

    query_embedding = model.encode([expanded])

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    ranked = []

    q = expanded.lower()

    for idx, sim in enumerate(similarities):

        item = catalog[idx]

        score = float(sim)

        name = item.get("name", "").lower()
        desc = item.get("description", "").lower()

        job_levels = " ".join(
            item.get("job_levels", [])
        ).lower()

        test_types = " ".join(
            item.get("keys", [])
        ).lower()

        # ------------------------
        # Keyword Boosting
        # ------------------------

        for word in q.split():

            if word in name:
                score += 0.60

            if word in desc:
                score += 0.30

            if word in job_levels:
                score += 0.20

            if word in test_types:
                score += 0.40

        ranked.append((idx, score))

    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    seen = set()

    for idx, score in ranked:

        item = catalog[idx]

        name = item.get("name")

        if name in seen:
            continue

        seen.add(name)

        results.append(item)

        if len(results) == top_k:
            break

    return results