import os
import glob
import logging
import tempfile
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

import sounddevice as sd
import soundfile as sf
from PyPDF2 import PdfReader
# Removed imports that are now in separate modules

import config
from client import LLMClient, EmbeddingClient, MilvusClient, AssemblyAIClient
from crewai_workflows import CrewAIClient, DataIngestionFlow, MultimodalRAGFlow
from command import CommandHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize client instances
llm_client = LLMClient()
embedding_client = EmbeddingClient()
assemblyai_client = AssemblyAIClient()
crewai_client = CrewAIClient()
milvus_client = MilvusClient()

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    获取文本嵌入向量，使用Ollama本地模型
    """
    return embedding_client.get_embeddings(texts)

# Global variables for caching
_collection = None

# Constants and classes moved to separate modules


def get_collection():
    """Get or create collection"""
    return milvus_client.get_collection()


def transcribe_audio_file(audio_file: str) -> str:
    """Transcribe audio file using AssemblyAI"""
    return assemblyai_client.transcribe_audio_file(audio_file)


def search_vector_database(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search vector database for relevant information"""
    # Generate query embedding
    embeddings = get_embeddings([query])
    query_embedding = embeddings[0]
    
    # Search using milvus_client
    return milvus_client.search_vectors(query_embedding, limit)


def format_search_results(search_results: List[Dict[str, Any]]) -> str:
    """Format search results into readable string"""
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


# SearchKnowledgeBaseTool moved to multimodal_rag_flow.py

# DataIngestionFlow and MultimodalRAGFlow moved to separate modules


def record_audio(duration: int = 10, sample_rate: int = 16000) -> str:
    """Record audio from microphone and save to temporary file"""
    print(f"🎤 Recording for {duration} seconds... Speak now!")
    print("Press Ctrl+C to stop early")
    
    try:
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
        sd.wait()
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        sf.write(temp_file.name, audio_data, sample_rate)
        
        print("✅ Recording completed!")
        return temp_file.name
        
    except KeyboardInterrupt:
        print("\n⏹️ Recording stopped by user")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        sf.write(temp_file.name, audio_data, sample_rate)
        return temp_file.name
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        raise


# process_query function moved to Command pattern implementation

def check_system_status():
    """Check if the system is ready"""
    return milvus_client.check_system_status()


def main():
    """Main application entry point"""
    print("\n🤖 Welcome to Multimodal Agentic RAG System!")
    print("=" * 50)
    
    # Validate API keys
    if not config.ASSEMBLYAI_API_KEY:
        print("\n❌ Missing API keys!")
        print("Please create a .env file with:")
        print("ASSEMBLYAI_API_KEY=your_key_here")
        return
    
    # Check system status and setup if needed
    print("🔍 Checking system status...")
    try:
        if check_system_status():
            print("✅ System ready!")
        else:
            print("\n⚠️ System not set up yet. Let's set it up first!")
            print("📡 Connecting to Milvus...")
            
            # Use Command pattern for system setup
            from command_pattern import SystemSetupCommand
            setup_command = SystemSetupCommand()
            setup_result = setup_command.execute()
            print(setup_result)
                
    except Exception as e:
        print(f"\n⚠️ Error checking system status: {e}")
        print("Make sure Milvus is running: docker-compose up -d")
        return
    
    # Main interaction loop using Command pattern
    command_handler = CommandHandler(record_audio_func=record_audio)
    
    while True:
        command_handler.show_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        # Get command based on user choice
        command = command_handler.get_command(choice)
        
        if command is not None:
            print("\n🤔 Processing...")
            result = command_handler.execute_command(command)
            
            # Check if user wants to exit
            if result == "EXIT":
                print("\n👋 Goodbye!")
                break
            
            # Display result if not empty
            if result:
                print(f"\n🤖 Response:\n{result}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc() 