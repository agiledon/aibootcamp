"""
数据摄取流程模块
负责文档发现、处理和向量数据库存储
"""

import logging
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from PyPDF2 import PdfReader
from pymilvus import Collection, FieldSchema, CollectionSchema, DataType, utility
from crewai.flow.flow import Flow, start, listen

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from client import MilvusClient, AssemblyAIClient, EmbeddingClient

logger = logging.getLogger(__name__)

# File patterns and extensions
FILE_PATTERNS = ["*.pdf", "*.mp3", "*.wav", "*.m4a", "*.flac", "*.txt", "*.md"]
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.flac'}
TEXT_EXTENSIONS = {'.txt', '.md'}


@dataclass
class DataIngestionState:
    """State for data ingestion flow"""
    discovered_files: Optional[List[str]] = None
    collection: Optional[Collection] = None
    chunks: List[Dict[str, Any]] = field(default_factory=list)
    processed_files: List[str] = field(default_factory=list)


class DataIngestionFlow(Flow):
    """CrewAI Flow for data ingestion and vector database setup"""
    
    def __init__(self):
        super().__init__()
        self.milvus_client = MilvusClient()
        self.assemblyai_client = AssemblyAIClient()
        self.embedding_client = EmbeddingClient()
    
    @start()
    def discover_files(self) -> DataIngestionState:
        """Discover all files in the data directory"""
        logger.info("🔍 Discovering files in data directory...")
        data_dir = Path(config.DATA_DIR)
        
        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")
        
        discovered_files = []
        for pattern in FILE_PATTERNS:
            files = glob.glob(str(data_dir / pattern))
            discovered_files.extend(files)
        
        discovered_files = sorted(list(set(discovered_files)))
        logger.info(f"📁 Discovered {len(discovered_files)} files")
        return DataIngestionState(discovered_files=discovered_files)
    
    @listen(lambda state: state.discovered_files is not None)
    def setup_vector_database(self, state: DataIngestionState) -> DataIngestionState:
        """Initialize Milvus connection and collection"""
        logger.info("🔧 Setting up vector database...")
        
        collection = self.milvus_client.get_collection()
        logger.info("✅ Vector database setup completed")
        
        return DataIngestionState(discovered_files=state.discovered_files, collection=collection)
    
    @listen(lambda state: state.collection is not None)
    def process_multimodal_data(self, state: DataIngestionState) -> DataIngestionState:
        """Process discovered files from the data directory"""
        logger.info(f"📄 Processing {len(state.discovered_files)} discovered files...")
        
        chunks = []
        processed_files = []
        
        for file_path in state.discovered_files:
            file_path = Path(file_path)
            filename = file_path.name
            logger.info(f"🔄 Processing: {filename}")
            
            try:
                # Process different file types
                if file_path.suffix.lower() == '.pdf':
                    with open(file_path, 'rb') as f:
                        reader = PdfReader(f)
                        text = "\n".join(page.extract_text() for page in reader.pages)
                    content_type = "pdf"
                elif file_path.suffix.lower() in AUDIO_EXTENSIONS:
                    text = self.assemblyai_client.transcribe_audio_file(str(file_path))
                    content_type = "audio"
                elif file_path.suffix.lower() in TEXT_EXTENSIONS:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    content_type = "text"
                else:
                    logger.warning(f"⚠️ Skipping unsupported file: {filename}")
                    continue
                
                # Create chunks
                chunk_size = 1000
                for i in range(0, len(text), chunk_size):
                    chunk = text[i:i + chunk_size]
                    if chunk.strip():
                        chunks.append({
                            "text": chunk,
                            "source": filename,
                            "content_type": content_type
                        })
                        
                processed_files.append(filename)
                        
            except Exception as e:
                logger.error(f"❌ Error processing {filename}: {e}")
                continue
        
        if not chunks:
            logger.warning("No content extracted from files")
            return DataIngestionState(
                discovered_files=state.discovered_files,
                collection=state.collection,
                chunks=[],
                processed_files=[]
            )
        
        logger.info(f"✅ Processed {len(chunks)} chunks from {len(processed_files)} files")
        return DataIngestionState(
            discovered_files=state.discovered_files,
            collection=state.collection,
            chunks=chunks,
            processed_files=processed_files
        )
    
    @listen(lambda state: len(state.chunks) > 0)
    def generate_embeddings_flow(self, state: DataIngestionState) -> DataIngestionState:
        """Generate embeddings for processed chunks"""
        logger.info(f"🧠 Generating embeddings for {len(state.chunks)} chunks...")
        
        texts = [chunk["text"] for chunk in state.chunks]
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_embeddings = self.embedding_client.get_embeddings(batch_texts)
            all_embeddings.extend(batch_embeddings)
        
        # Assign embeddings to chunks
        updated_chunks = []
        for chunk, embedding in zip(state.chunks, all_embeddings):
            chunk_copy = chunk.copy()
            chunk_copy["embedding"] = embedding
            updated_chunks.append(chunk_copy)
        
        logger.info("✅ Embeddings generation completed")
        return DataIngestionState(
            discovered_files=state.discovered_files,
            collection=state.collection,
            chunks=updated_chunks,
            processed_files=state.processed_files
        )
    
    @listen(lambda state: all(chunk.get("embedding") is not None for chunk in state.chunks))
    def store_in_vector_database(self, state: DataIngestionState) -> DataIngestionState:
        """Insert processed chunks into Milvus"""
        logger.info(f"💾 Inserting {len(state.chunks)} chunks into vector database...")
        
        data = [
            [chunk["text"] for chunk in state.chunks],  # content
            [chunk.get("source_type", "unknown") for chunk in state.chunks],  # source_type
            [chunk["source"] for chunk in state.chunks],  # source
            [chunk["content_type"] for chunk in state.chunks],  # content_type
            [chunk["embedding"] for chunk in state.chunks]  # embedding
        ]
        
        self.milvus_client.insert_vectors(data)
        logger.info("✅ Data insertion completed")
        return state
