"""
Client modules for various services and APIs.

This module contains client implementations for:
- LLM Client: Language model interactions
- Embedding Client: Text embedding generation
- Milvus Client: Vector database operations
- AssemblyAI Client: Audio transcription services
"""

# Use lazy imports to avoid circular import issues
def __getattr__(name):
    if name == 'LLMClient':
        from .llm_client import LLMClient
        return LLMClient
    elif name == 'EmbeddingClient':
        from .embedding_client import EmbeddingClient
        return EmbeddingClient
    elif name == 'MilvusClient':
        from .milvus_client import MilvusClient
        return MilvusClient
    elif name == 'AssemblyAIClient':
        from .assemblyai_client import AssemblyAIClient
        return AssemblyAIClient
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    'LLMClient',
    'EmbeddingClient', 
    'MilvusClient',
    'AssemblyAIClient'
]
