"""
Workflow implementations for multimodal RAG processing.

This module contains:
- CrewAI Client: Multi-agent system integration
- Data Ingestion Flow: Handles document and audio processing workflows
- Multimodal RAG Flow: Orchestrates retrieval-augmented generation processes
"""

# Use lazy imports to avoid circular import issues
def __getattr__(name):
    if name == 'CrewAIClient':
        from .crewai_client import CrewAIClient
        return CrewAIClient
    elif name == 'DataIngestionFlow':
        from .data_ingestion_flow import DataIngestionFlow
        return DataIngestionFlow
    elif name == 'MultimodalRAGFlow':
        from .multimodal_rag_flow import MultimodalRAGFlow
        return MultimodalRAGFlow
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    'CrewAIClient',
    'DataIngestionFlow',
    'MultimodalRAGFlow'
]
