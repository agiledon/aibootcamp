# CrewAI Flow Multimodal

A multimodal RAG (Retrieval-Augmented Generation) system based on CrewAI that supports processing and querying documents and audio files.

## Features

- **Multimodal Support**: Supports PDF documents and audio files (MP3, WAV, M4A, FLAC)
- **Intelligent Processing**: Uses CrewAI multi-agent collaboration for document processing
- **Vector Retrieval**: Semantic search based on Milvus vector database
- **Speech-to-Text**: Audio transcription using AssemblyAI
- **Unified LLM**: All components (CrewAI, direct LLM calls) use DeepSeek models
- **Intelligent Q&A**: Intelligent question-answering system based on DeepSeek models

## Architecture

The system consists of several key components:

- **CrewAI Agents**: Multi-agent collaboration for document processing and analysis
- **Milvus Vector Database**: High-performance vector storage and retrieval
- **AssemblyAI Integration**: Real-time audio transcription services
- **DeepSeek LLM**: Unified language model for all text generation tasks
- **Ollama Embeddings**: Local embedding model for vector generation

## Environment Setup

### 1. Create .env File

Create a `.env` file in the project root directory with the following configuration:

```bash
# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here
LLM_MODEL=deepseek-chat
LLM_API_BASE=https://api.deepseek.com

# AssemblyAI API Configuration
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here

# Milvus Vector Database Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
MILVUS_COLLECTION_NAME=multimodal_rag

# Embedding Model Configuration (Ollama Local Model)
EMBEDDING_MODEL=nomic-embed-text:latest
EMBEDDING_DIMENSION=768
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. API Key Setup

#### DeepSeek API
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Register an account and obtain API key
3. Add the key to `DEEPSEEK_API_KEY`

#### Ollama (Embedding Model)
1. Install Ollama: https://ollama.ai/
2. Download embedding model: `ollama pull nomic-embed-text:latest`
3. Ensure Ollama service is running: `ollama serve`

#### AssemblyAI API
1. Visit [AssemblyAI](https://www.assemblyai.com/)
2. Register an account and obtain API key
3. Add the key to `ASSEMBLYAI_API_KEY`

### 3. Install Dependencies

```bash
# Install dependencies using uv
uv sync

# Or install using pip
pip install -r requirements.txt
```

### 4. Start Services

#### Option 1: Use Existing Milvus Service
If you already have Milvus service running on your system:

```bash
# Check Milvus service status
docker ps | grep milvus

# If Milvus is running, start the main program directly
python main.py
```

#### Option 2: Start New Milvus Service
If you need to start a new Milvus service:

```bash
# Start Milvus database (using Docker)
docker-compose up -d

# Run the main program
python main.py
```

### 5. System Testing

Before first run, it's recommended to run the system test script:

```bash
# Run system tests
python test_system.py
```

The test script will check:
- ✅ All dependency packages are correctly installed
- ✅ Configuration files are correct
- ✅ API keys are configured
- ✅ Milvus connection is normal
- ✅ Ollama embedding model connection is normal
- ✅ Embedding dimension consistency (768 dimensions)

## Usage

### Basic Usage

1. **Start the system**:
   ```bash
   python main.py
   ```

2. **Upload documents**: Place your PDF files in the `data/` directory

3. **Upload audio files**: Place your audio files (MP3, WAV, etc.) in the `data/` directory

4. **Query the system**: Use the interactive interface to ask questions about your documents

### Advanced Usage

The system supports various query types:

- **Document-based queries**: Ask questions about PDF content
- **Audio-based queries**: Ask questions about transcribed audio content
- **Cross-modal queries**: Ask questions that span multiple document types
- **Temporal queries**: Ask about content changes over time

## File Structure

```
├── main.py                    # Main program file
├── config.py                  # Configuration file
├── crewai_client.py           # CrewAI integration client
├── llm_client.py              # LLM client wrapper
├── embedding_client.py        # Embedding model client
├── milvus_client.py           # Milvus vector database client
├── assemblyai_client.py       # AssemblyAI transcription client
├── multimodal_rag_flow.py     # Multimodal RAG workflow
├── data_ingestion_flow.py     # Data ingestion workflow
├── command_handler.py         # Command pattern handler
├── command_pattern.py         # Command pattern implementation
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker service configuration
├── data/                      # Data files directory
│   ├── annualreport-2024.pdf # Sample PDF document
│   └── finance_audio.mp3     # Sample audio file
└── .env                       # Environment variables configuration
```

## Technical Details

### Multimodal Processing Pipeline

1. **Document Processing**: PDFs are parsed and chunked for optimal retrieval
2. **Audio Processing**: Audio files are transcribed using AssemblyAI
3. **Embedding Generation**: Text chunks are converted to vectors using Ollama
4. **Vector Storage**: Embeddings are stored in Milvus with metadata
5. **Query Processing**: User queries are processed through the same pipeline
6. **Retrieval**: Relevant chunks are retrieved based on semantic similarity
7. **Generation**: Final answers are generated using DeepSeek LLM

### Performance Optimizations

- **Batch Processing**: Multiple documents processed in parallel
- **Caching**: Embedding results cached to avoid recomputation
- **Indexing**: Optimized Milvus indexes for fast retrieval
- **Memory Management**: Efficient memory usage for large document sets

## Troubleshooting

### Common Issues

1. **Milvus Connection Failed**:
   - Ensure Milvus service is running
   - Check connection parameters in `.env`
   - Verify network connectivity

2. **Ollama Embedding Model Not Found**:
   - Run `ollama pull nomic-embed-text:latest`
   - Check Ollama service status
   - Verify model name in configuration

3. **API Key Issues**:
   - Verify API keys are correctly set in `.env`
   - Check API quotas and billing
   - Ensure network access to API endpoints

### Performance Tuning

- **Embedding Dimension**: Adjust `EMBEDDING_DIMENSION` based on your needs
- **Chunk Size**: Modify chunk size for optimal retrieval performance
- **Batch Size**: Adjust batch processing size based on available memory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Contributors

### Zhang Yi
AI Strategy Consultant and AI-Native Application Developer, DDD Evangelist, Enterprise Mentor at Nanjing University DevOps+ Research Lab.

- GitHub: [@agiledon](https://github.com/agiledon)

### Original Project Credits
This repository is based on and significantly refactored from the [multimodal-rag-assemblyai](https://github.com/patchy631/ai-engineering-hub) project in the [AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub). 

**Key Improvements and Enhancements:**
- **Code Refactoring**: Complete architectural redesign with improved modularity and maintainability
- **DeepSeek Integration**: Full support for DeepSeek LLM models as the primary language model
- **Ollama Local Deployment**: Integration with Ollama for local deployment of nomic-embed-text embedding models
- **Enhanced Multimodal Processing**: Improved document and audio processing workflows
- **Advanced RAG Pipeline**: Optimized retrieval-augmented generation with better performance
- **CrewAI Integration**: Enhanced multi-agent collaboration for document processing
- **Production-Ready**: Better error handling, logging, and deployment configurations

We extend our gratitude to the original contributors of the AI Engineering Hub for providing the foundational multimodal RAG implementation.

## License

This repository is licensed under the MIT License - see the LICENSE file for details.

## Notes

1. **Embedding Model Limitation**: DeepSeek API currently doesn't support embedding models, so OpenAI's text-embedding-3-small model is used
2. **Network Requirements**: Requires access to DeepSeek, OpenAI, and AssemblyAI API services
3. **Milvus Database**: Milvus database service must be running for vector retrieval functionality to work properly
4. **Resource Requirements**: Ensure sufficient memory and CPU resources for optimal performance

## Support

For issues and questions, please open an issue in the repository or contact the development team.