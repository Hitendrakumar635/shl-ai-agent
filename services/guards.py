OFF_TOPIC = [
    "weather",
    "football",
    "cricket",
    "movie",
    "news",
    "politics",
    "recipe",
    "joke",
    "ipl",
    "bitcoin"
]

PROMPT_INJECTION = [
    "ignore previous",
    "ignore all instructions",
    "system prompt",
    "developer message",
    "reveal prompt",
    "forget instructions",
    "act as"
]


def is_off_topic(query: str):

    query = query.lower()

    return any(word in query for word in OFF_TOPIC)


def is_prompt_injection(query: str):

    query = query.lower()

    return any(word in query for word in PROMPT_INJECTION)