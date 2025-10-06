"""
多模态RAG流程模块
负责查询处理、知识库搜索和响应生成
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from crewai.flow.flow import Flow, start, listen
from crewai.tools import BaseTool

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from .crewai_client import CrewAIClient
from client import AssemblyAIClient, EmbeddingClient, MilvusClient

logger = logging.getLogger(__name__)


@dataclass
class QueryState:
    """State for query processing flow"""
    query: str = ""
    audio_file: Optional[str] = None
    transcribed_query: Optional[str] = None
    search_results: str = ""
    final_response: str = ""


class SearchKnowledgeBaseTool(BaseTool):
    """Custom tool for searching the knowledge base"""
    
    name: str = "search_knowledge_base"
    description: str = "Search the knowledge base for relevant information based on a query"
    
    def __init__(self):
        super().__init__()
        # Initialize clients inside the tool
        self._embedding_client = EmbeddingClient()
        self._milvus_client = MilvusClient()
    
    def _run(self, query: str) -> str:
        """Execute the search in the knowledge base"""
        try:
            # Generate query embedding
            embeddings = self._embedding_client.get_embeddings([query])
            query_embedding = embeddings[0]
            
            # Search using milvus_client
            search_results = self._milvus_client.search_vectors(query_embedding, limit=5)
            
            # Format results
            if not search_results:
                return "No relevant documents found."
            
            formatted_results = []
            for result in search_results:
                relevance = (1 - result['distance']) * 100
                formatted_results.append(
                    f"Source: {result['source']} ({result['content_type']})\n"
                    f"Relevance: {relevance:.1f}%\n"
                    f"Content: {result['content'][:200]}...\n"
                    f"---"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Error in search tool: {e}")
            return f"Error searching knowledge base: {str(e)}"


class MultimodalRAGFlow(Flow):
    """CrewAI Flow for query processing and response generation"""
    
    def __init__(self):
        super().__init__()
        self.crewai_client = CrewAIClient()
        self.assemblyai_client = AssemblyAIClient()
        self.embedding_client = EmbeddingClient()
        self.milvus_client = MilvusClient()
    
    @start()
    def transcribe_audio_if_needed(self, inputs: dict = None) -> QueryState:
        """Transcribe audio if query is audio-based"""
        # Extract inputs from kickoff parameters
        if inputs:
            query = inputs.get("query", "")
            audio_file = inputs.get("audio_file", None)
        else:
            query = ""
            audio_file = None
            
        if audio_file:
            logger.info("🎤 Transcribing audio file...")
            transcribed_query = self.assemblyai_client.transcribe_audio_file(audio_file)
            logger.info(f"✅ Transcribed: {transcribed_query}")
        else:
            transcribed_query = query
            logger.info("📝 Using text query directly")
        
        return QueryState(query=query, audio_file=audio_file, transcribed_query=transcribed_query)
    
    @listen(lambda state: state.transcribed_query is not None)
    def search_knowledge_base(self, state: QueryState) -> QueryState:
        """Search the vector database for relevant information"""
        logger.info("🔍 Searching knowledge base...")
        
        # Generate query embedding
        embeddings = self.embedding_client.get_embeddings([state.transcribed_query])
        query_embedding = embeddings[0]
        
        # Search using milvus_client
        search_results = self.milvus_client.search_vectors(query_embedding, limit=5)
        
        # Format results
        if not search_results:
            formatted_results = "No relevant documents found."
        else:
            formatted_results = []
            for result in search_results:
                relevance = (1 - result['distance']) * 100
                formatted_results.append(
                    f"Source: {result['source']} ({result['content_type']})\n"
                    f"Relevance: {relevance:.1f}%\n"
                    f"Content: {result['content'][:200]}...\n"
                    f"---"
                )
            formatted_results = "\n".join(formatted_results)
        
        logger.info("✅ Search completed")
        
        return QueryState(
            query=state.query,
            audio_file=state.audio_file,
            transcribed_query=state.transcribed_query,
            search_results=formatted_results
        )
    
    @listen(lambda state: state.search_results is not None)
    def generate_response(self, state: QueryState) -> QueryState:
        """Generate final response using CrewAI agents"""
        logger.info("🤖 Generating response...")
        
        try:
            # Create agents using crewai_client
            research_agent = self.crewai_client.create_agent(
                role="Information Retrieval Specialist",
                goal="Find the most relevant information from the knowledge base to answer user queries",
                backstory="You are an expert at analyzing queries and searching through multimodal knowledge bases to find the most relevant information.",
                tools=[SearchKnowledgeBaseTool()]
            )
            
            response_agent = self.crewai_client.create_agent(
                role="Response Generator",
                goal="Generate comprehensive, accurate, and helpful responses based on retrieved information",
                backstory="You are an expert at synthesizing information from multiple sources and creating clear, informative responses."
            )
            
            # Create tasks using crewai_client
            research_task = self.crewai_client.create_task(
                description=f"Search for information relevant to: '{state.transcribed_query}'. Use the search_knowledge_base tool to find the most relevant context.",
                agent=research_agent,
                expected_output="Detailed information from the knowledge base with proper citations"
            )
            
            response_task = self.crewai_client.create_task(
                description=f"Based on the research findings, generate a comprehensive response to: '{state.transcribed_query}'.",
                agent=response_agent,
                expected_output="A well-structured, comprehensive response with proper citations"
            )
            
            # Create crew and execute
            crew = self.crewai_client.create_crew(
                agents=[research_agent, response_agent],
                tasks=[research_task, response_task]
            )
            
            result = crew.kickoff()
            logger.info("✅ Response generated")
            
            return QueryState(
                query=state.query,
                audio_file=state.audio_file,
                transcribed_query=state.transcribed_query,
                search_results=state.search_results,
                final_response=result
            )
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Fallback response
            fallback_response = f"Based on the search results:\n{state.search_results}\n\nQuery: {state.transcribed_query}"
            return QueryState(
                query=state.query,
                audio_file=state.audio_file,
                transcribed_query=state.transcribed_query,
                search_results=state.search_results,
                final_response=fallback_response
            )
