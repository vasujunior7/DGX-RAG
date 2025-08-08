# Legal Query RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system specifically designed for legal document analysis and query processing. This system supports parallel inference for 15-20 queries simultaneously and implements the complete Legal Query RAG pipeline as described in the research paper.

## 🌟 Features

- **Parallel Query Processing**: Handle 15-20 legal queries simultaneously with optimized async processing
- **Complete RAG Pipeline**: Implements all stages from document ingestion to response evaluation
- **Legal Domain Optimized**: Specialized for legal document analysis and query understanding
- **Quality Assurance**: Built-in response evaluation and improvement loops
- **Hybrid Retrieval**: Combines semantic search with keyword-based BM25 retrieval
- **ReAct Agent**: Intelligent query processing and reasoning
- **Document Re-ranking**: Cross-encoder re-ranking for improved relevance

## 📋 System Architecture

### Pipeline Stages

1. **Data Ingestion**: Process legal documents (PDFs, text files)
2. **Embedding Generation**: Create dense vector embeddings using OpenAI models
3. **Vector Database**: Store and index embeddings using FAISS
4. **Query Processing**: ReAct agent for query understanding and refinement
5. **Hybrid Retrieval**: Semantic + keyword search for comprehensive results
6. **Document Re-ranking**: Cross-encoder re-ranking for relevance
7. **Response Generation**: LLM-based answer generation using retrieved context
8. **Quality Evaluation**: Automated response quality assessment
9. **Feedback Loop**: Iterative improvement based on evaluation

## 🚀 Quick Start

### Installation

1. Clone the repository and navigate to the project directory:

```bash
cd SAM_model
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

```python
from infrance import LegalRAGInference
import asyncio

async def main():
    # Initialize the system
    legal_rag = LegalRAGInference(api_key="your-openai-api-key")

    # Load legal documents
    document_paths = [
        "path/to/legal_document_1.pdf",
        "path/to/legal_document_2.txt",
        # Add more document paths...
    ]
    await legal_rag.load_documents(document_paths)

    # Process multiple queries in parallel
    queries = [
        "What are the elements of a valid contract?",
        "How is negligence established in tort law?",
        "What are the requirements for adverse possession?",
        # Add up to 15-20 queries for parallel processing...
    ]

    results = await legal_rag.async_inference(queries)

    # Display results
    for result in results:
        print(f"Query: {result['original_query']}")
        print(f"Answer: {result['response']['answer']}")
        print(f"Quality Score: {result['evaluation']['overall_score']}/10")
        print("-" * 80)

# Run the example
asyncio.run(main())
```

### Synchronous Usage (Backward Compatibility)

```python
from infrance import LegalRAGInference

# Initialize
legal_rag = LegalRAGInference(api_key="your-openai-api-key")

# Load documents (synchronous)
legal_rag.load_document("path/to/document.pdf")

# Simple inference
questions = ["What constitutes breach of contract?"]
answers = legal_rag.inference(questions)
print(answers[0])
```

## 📁 Project Structure

```
SAM_model/
├── src/                          # Core system modules
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── data_ingestion.py        # Document loading and preprocessing
│   ├── embeddings.py            # OpenAI embedding generation
│   ├── vector_db.py             # FAISS vector database
│   ├── react_agent.py           # ReAct query processing agent
│   ├── retrieval.py             # Hybrid retrieval system
│   ├── reranking.py             # Document re-ranking
│   ├── llm_generator.py         # Response generation
│   ├── evaluation.py            # Response quality evaluation
│   └── legal_query_rag.py       # Main system integration
├── infrance.py                  # Main inference interface
├── example_usage.py             # Comprehensive usage examples
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## ⚙️ Configuration

The system can be configured by modifying `src/config.py` or environment variables:

### Key Configuration Options

- **Models**:

  - `EMBEDDING_MODEL`: OpenAI embedding model (default: "text-embedding-3-small")
  - `LLM_MODEL`: Chat completion model (default: "gpt-3.5-turbo")
  - `EVALUATION_MODEL`: Evaluation model (default: "gpt-4o")

- **Performance**:

  - `MAX_CONCURRENT_QUERIES`: Maximum parallel queries (default: 20)
  - `BATCH_SIZE`: Embedding batch size (default: 5)
  - `TOP_K_RETRIEVAL`: Number of documents to retrieve (default: 10)

- **Quality**:
  - `SIMILARITY_THRESHOLD`: Minimum similarity for retrieval (default: 0.7)
  - `MIN_ANSWER_QUALITY_SCORE`: Minimum quality score (default: 0.7)

## 🔧 Advanced Usage

### Custom Configuration

```python
from src.config import Config

# Create custom configuration
config = Config()
config.LLM_MODEL = "gpt-4o"
config.MAX_CONCURRENT_QUERIES = 15
config.CHUNK_SIZE = 800

# Initialize with custom config
legal_rag = LegalRAGInference()
legal_rag.config = config
```

### Single Query with Quality Improvement

```python
# Process single query with iterative improvement
result = await legal_rag.single_query_inference(
    "What is the statute of limitations for contract disputes?",
    max_iterations=3
)

print(f"Final quality score: {result['evaluation']['overall_score']}/10")
print(f"Iterations needed: {result['iterations']}")
```

### Knowledge Base Management

```python
# Save knowledge base for reuse
legal_rag.save_knowledge_base("my_legal_kb")

# Load existing knowledge base
legal_rag.load_knowledge_base("my_legal_kb")

# Add new documents to existing knowledge base
await legal_rag.add_documents(["new_document.pdf"])
```

## 📊 Performance Optimization

### Parallel Processing Tips

1. **Optimal Batch Size**: 15-20 queries for best performance/cost balance
2. **Concurrent Limits**: Adjust `MAX_CONCURRENT_QUERIES` based on API limits
3. **Embedding Batching**: Use `BATCH_SIZE` to optimize embedding API calls
4. **Caching**: Save/load knowledge bases to avoid reprocessing documents

### Memory Management

- Large document collections: Consider chunking strategy
- Vector database: FAISS provides efficient similarity search
- Re-ranking: Limited to top-k documents to manage computational cost

## 🏗️ System Requirements

### Required Dependencies

- **Python**: 3.8+
- **OpenAI API**: GPT models and embeddings
- **LangChain**: Document processing and LLM integration
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Re-ranking models

### Optional Dependencies

- **Pinecone/Weaviate**: Alternative vector databases
- **Tesseract**: OCR for scanned documents
- **spaCy**: Advanced NLP processing

## 🧪 Testing

Run the example script to test the system:

```bash
python example_usage.py
```

This will demonstrate:

- Parallel processing of 20 legal queries
- Complete RAG pipeline execution
- Quality evaluation and scoring
- Performance metrics and statistics

## 📈 Monitoring and Evaluation

The system provides comprehensive metrics:

- **Performance**: Processing time, queries per second
- **Quality**: Accuracy, completeness, relevance scores
- **System**: Document count, embedding statistics
- **Evaluation**: Pass rates, improvement suggestions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 References

Based on the Legal Query RAG research paper and implements the complete pipeline for legal document analysis and retrieval-augmented generation.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Not Set**: Ensure `OPENAI_API_KEY` environment variable is set
2. **Memory Issues**: Reduce batch size or chunk size for large documents
3. **Slow Performance**: Check API rate limits and adjust concurrent queries
4. **Quality Issues**: Ensure high-quality legal documents in knowledge base

### Support

For issues and questions, please check the example usage script and configuration options first.
