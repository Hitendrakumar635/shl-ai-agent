from fastapi import FastAPI
from models.schemas import ChatRequest, ChatResponse
from services.catalog import load_catalog
from services.agent import chat

app = FastAPI(
    title="SHL AI Assessment Recommendation API",
    version="1.0.0"
)

# Load SHL catalog when application starts
catalog = load_catalog()


@app.get("/")
def home():
    return {
        "message": "SHL AI Hiring Assistant API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/catalog/count")
def catalog_count():
    return {
        "total_items": len(catalog)
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    messages = []

    for message in request.messages:
        messages.append({
            "role": message.role,
            "content": message.content
        })

    result = chat(messages)

    return result