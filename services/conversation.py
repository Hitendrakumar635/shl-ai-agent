def get_latest_user_message(messages):
    """
    Returns latest user message.
    """
    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"]

    return ""


def extract_context(messages):
    """
    Converts full conversation into text.
    """
    history = []

    for message in messages:
        role = message["role"].capitalize()
        history.append(f"{role}: {message['content']}")

    return "\n".join(history)


def needs_clarification(user_query: str):
    """
    Returns True if query is too vague.
    """

    query = user_query.lower().strip()

    vague_queries = [
        "assessment",
        "test",
        "exam",
        "hire",
        "hiring",
        "need a test",
        "recommend assessment",
        "assessment for hiring",
        "recommend",
        "help",
    ]

    if len(query.split()) <= 3:
        return True

    if query in vague_queries:
        return True

    return False


def is_end_of_conversation(user_query: str):
    """
    Detects conversation ending.
    """

    query = user_query.lower().strip()

    endings = [
        "thanks",
        "thank you",
        "ok thanks",
        "okay thanks",
        "no thanks",
        "that's all",
        "thats all",
        "done",
        "bye",
        "goodbye",
        "nothing else",
        "resolved",
    ]

    return query in endings