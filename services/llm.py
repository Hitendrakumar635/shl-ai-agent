import google.generativeai as genai

from config import GEMINI_API_KEY

# Configure Gemini only if API key exists
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    model = None


DEFAULT_REPLY = (
    "I found matching SHL assessments based on your request. "
    "Please review the recommendations below."
)


def ask_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    Returns a reply from Gemini.
    Never returns None.
    """

    if model is None:
        return DEFAULT_REPLY

    try:
        prompt = f"""
{system_prompt}

----------------------------

{user_prompt}
"""

        response = model.generate_content(prompt)

        if (
            response
            and hasattr(response, "text")
            and response.text
            and response.text.strip()
        ):
            return response.text.strip()

        return DEFAULT_REPLY

    except Exception as e:
        print("\nGemini Error:", e, "\n")
        return DEFAULT_REPLY