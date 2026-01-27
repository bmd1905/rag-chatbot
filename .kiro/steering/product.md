# Product Overview

RAG Chatbot is a conversational AI application that uses Retrieval-Augmented Generation to answer questions based on a knowledge base.

## Core Functionality

- Chat interface for user queries
- Vector-based document retrieval using ChromaDB
- LLM-powered response generation via OpenAI GPT-4o-mini
- Source attribution for transparency

## Architecture

- FastAPI backend serving both API and static frontend
- Single-page HTML/JS frontend with inline styling
- In-memory vector store seeded with sample documents at startup
