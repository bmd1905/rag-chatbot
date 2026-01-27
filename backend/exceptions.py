"""Custom exceptions for the RAG Chatbot."""


class ChatbotError(Exception):
    """Base exception for all chatbot-related errors."""

    pass


class ConfigurationError(ChatbotError):
    """Raised when configuration is invalid or missing."""

    pass


class RetrievalError(ChatbotError):
    """Raised when document retrieval fails."""

    pass


class EmbeddingError(ChatbotError):
    """Raised when embedding generation fails."""

    pass


class ModelError(ChatbotError):
    """Raised when LLM model operations fail."""

    pass


class ValidationError(ChatbotError):
    """Raised when input validation fails."""

    pass
