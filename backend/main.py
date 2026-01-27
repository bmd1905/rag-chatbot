from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

from backend.agent import add_documents, run_agent
from backend.schemas import ChatRequest, ChatResponse

app = FastAPI(title="RAG Chatbot")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Seed with sample documents
add_documents(
    [
        "RAG (Retrieval-Augmented Generation) combines retrieval with generation for accurate responses.",
        "Vector databases store embeddings for semantic search.",
        "LLMs can be enhanced with external knowledge through RAG pipelines.",
    ]
)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response, sources = run_agent(request.message)
    return ChatResponse(response=response, sources=sources)


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


app.mount("/static", StaticFiles(directory="frontend"), name="static")
