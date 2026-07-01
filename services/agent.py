from services.retriever import search_assessments
from services.llm import ask_gemini
from services.prompts import SYSTEM_PROMPT

from services.conversation import (
    get_latest_user_message,
    extract_context,
    needs_clarification,
    is_end_of_conversation,
)

from services.guards import (
    is_off_topic,
    is_prompt_injection,
)

from services.comparison import compare_assessments
from services.refinement import is_refinement


def build_catalog_context(results):

    context = ""

    for item in results:

        context += f"""
Name: {item.get("name","")}
Description: {item.get("description","")}
Job Levels: {", ".join(item.get("job_levels",[]))}
Test Types: {", ".join(item.get("keys",[]))}
URL: {item.get("link","")}

"""

    return context


def build_recommendations(results):

    recommendations = []

    for item in results[:10]:

        recommendations.append(
            {
                "name": item.get("name"),
                "url": item.get("link"),
                "test_type": ", ".join(item.get("keys", [])),
            }
        )

    return recommendations


def chat(messages):

    if not messages:

        return {
            "reply": "Hello! How can I help you find the right SHL assessment today?",
            "recommendations": [],
            "end_of_conversation": False,
        }

    user_query = get_latest_user_message(messages)
    history = extract_context(messages)
    # ----------------------------
# End Conversation
# ----------------------------

    if is_end_of_conversation(user_query):
      return {
            "reply": "You're welcome! If you need help selecting SHL assessments in the future, feel free to ask.",
        "recommendations": [],
        "end_of_conversation": True,
    }

    # --------------------------------------------------
    # Prompt Injection Protection
    # --------------------------------------------------

    if is_prompt_injection(user_query):

        return {
            "reply": "Sorry, I can only help with SHL assessments. I cannot reveal system prompts or ignore my instructions.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    # --------------------------------------------------
    # Off-topic Refusal
    # --------------------------------------------------

    if is_off_topic(user_query):

        return {
            "reply": "I'm designed only to recommend and compare SHL assessments. Please ask me something related to SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    # --------------------------------------------------
    # Clarification
    # --------------------------------------------------

    if needs_clarification(user_query):

        return {
            "reply": (
                "Could you please provide a few more details?\n\n"
                "• Job Role\n"
                "• Experience Level\n"
                "• Required Skills\n\n"
                "This will help me recommend the most suitable SHL assessments."
            ),
            "recommendations": [],
            "end_of_conversation": False,
        }

    # --------------------------------------------------
    # Comparison
    # --------------------------------------------------
    comparison = compare_assessments(user_query)

    if comparison:

        lines = []

        for item in comparison:
            lines.append(
                f"""• {item.get('name')}

Test Type: {item.get('test_type', '')}

Job Levels: {item.get('job_levels', '')}

Description: {item.get('description', '')}
"""
            )

        reply = (
            "Comparison of the requested SHL assessments:\n\n"
            + "\n".join(lines)
        )

        recommendations = []

        for item in comparison:
            recommendations.append(
                {
                    "name": item.get("name"),
                    "url": item.get("url"),
                    "test_type": item.get("test_type", ""),
                }
            )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False,
        }
    

      
    # --------------------------------------------------
    # Refinement
    # --------------------------------------------------

    search_query = user_query

    if is_refinement(user_query):

        search_query = history

    # --------------------------------------------------
    # Semantic Retrieval
    # --------------------------------------------------

    results = search_assessments(search_query)

    if len(results) == 0:

        return {
            "reply": "I couldn't find any suitable SHL assessment. Could you provide more information?",
            "recommendations": [],
            "end_of_conversation": False,
        }

    catalog_context = build_catalog_context(results)

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

Conversation History

{history}

Available SHL Catalog

{catalog_context}

User Request

{user_query}

Rules

1. Recommend ONLY from catalog.
2. Never invent assessments.
3. Mention why each assessment matches.
4. Keep response under 150 words.
"""

    reply = ask_gemini(SYSTEM_PROMPT, prompt)

    recommendations = build_recommendations(results)

    end_conversation = False

    if len(messages) >= 4:
        end_conversation = True

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": end_conversation,
    }