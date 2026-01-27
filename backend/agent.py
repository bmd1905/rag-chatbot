import os

import chromadb
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("documents")


def add_documents(docs: list[str]) -> None:
    """Add documents to the vector store."""
    for i, doc in enumerate(docs):
        collection.add(documents=[doc], ids=[f"doc_{i}"])


def retrieve(query: str, k: int = 3) -> list[str]:
    """Retrieve relevant documents for a query."""
    results = collection.query(query_texts=[query], n_results=k)
    return results["documents"][0] if results["documents"] else []


def run_agent(query: str) -> tuple[str, list[str]]:
    """Run the agentic RAG pipeline."""
    # Retrieve relevant context
    context_docs = retrieve(query)
    context = "\n".join(context_docs) if context_docs else "No relevant documents found."

    # Agent system prompt with tool-use capability
    system_prompt = """You are a helpful assistant with access to a knowledge base.
Use the provided context to answer questions accurately.
If the context doesn't contain relevant information, say so.
Be concise and direct."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
    ]

    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.7, max_tokens=500)

    return response.choices[0].message.content, context_docs
