REFINEMENT_WORDS = [
    "actually",
    "instead",
    "also",
    "add",
    "remove",
    "change",
    "update"
]


def is_refinement(query):

    query = query.lower()

    return any(word in query for word in REFINEMENT_WORDS)