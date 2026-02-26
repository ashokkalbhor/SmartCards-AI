# SmartCards AI - Complete Setup Guide

A comprehensive guide to set up the SmartCards AI chatbot system with multi-source document processing and vector database integration.

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- OpenAI API Key
- Chrome browser (for web scraping)

### 2. Installation

```bash
# Clone repository and navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Run Complete Setup

```bash
# Process documents and set up vector database
python -m app.scripts.setup_complete_knowledge_base

# Test the system
python -m app.scripts.test_system --quick

# Start the API server
uvicorn app.main:app --reload
```

## 📋 Detailed Setup

### Step 1: Environment Configuration

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
CHROMA_DB_PATH=./chroma_db
OPENAI_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-ada-002
```

### Step 2: Document Sources Configuration

Edit `app/data/config/document_sources.yaml` to configure your document sources:

#### Option A: PDF URLs
```yaml
- type: "pdf_url"
  url: "https://bank.com/terms.pdf"
  document_category: "terms"
```

#### Option B: Web Pages (MITC)
```yaml
- type: "web_page"
  url: "https://bank.com/card-features"
  document_category: "features"
  scraping_config:
    selectors: [".card-benefits", ".features"]
```

#### Option C: Manual Upload
```yaml
- type: "upload"
  source_type: "pdf"
  file_path: "app/data/documents/uploads/card_terms.pdf"
  document_category: "terms"
```

### Step 3: Document Processing

```bash
# Process all configured document sources
python -m app.scripts.universal_document_processor

# Or run the complete setup
python -m app.scripts.setup_complete_knowledge_base
```

### Step 4: ChromaDB Ingestion

```bash
# Ingest processed documents into ChromaDB
python -m app.scripts.ingest_to_chroma

# Force re-ingestion if needed
python -m app.scripts.ingest_to_chroma --force
```

### Step 5: Verification

```bash
# Run system tests
python -m app.scripts.test_system

# Interactive testing
python -m app.scripts.test_system --interactive
```

## 📁 Directory Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/
│   │   └── chatbot.py          # Chatbot API endpoints
│   ├── core/
│   │   ├── ai_service.py       # AI service integration
│   │   ├── vector_db.py        # ChromaDB service
│   │   └── config.py           # Configuration
│   ├── data/
│   │   ├── config/
│   │   │   └── document_sources.yaml  # Document sources config
│   │   └── documents/
│   │       ├── uploads/        # Manual document uploads
│   │       ├── processed/      # Processed text files
│   │       ├── chunks/         # Document chunks for embedding
│   │       └── temp/           # Temporary downloads
│   ├── models/                 # Database models
│   └── scripts/
│       ├── universal_document_processor.py
│       ├── ingest_to_chroma.py
│       ├── setup_complete_knowledge_base.py
│       └── test_system.py
├── chroma_db/                  # ChromaDB storage
└── requirements.txt
```

## 🔧 Configuration Options

### Document Processing Settings

Edit `app/data/config/document_sources.yaml`:

```yaml
processing_config:
  chunk_size: 1000              # Characters per chunk
  chunk_overlap: 200            # Overlap between chunks
  max_retries: 3                # Retry failed downloads
  request_timeout: 30           # Timeout in seconds
```

### AI Service Settings

Edit `app/core/config.py`:

```python
# AI Settings
MAX_TOKENS: int = 2000
TEMPERATURE: float = 0.7
VECTOR_SEARCH_LIMIT: int = 5
FALLBACK_TO_LLM_THRESHOLD: float = 0.6
```

## 📊 Usage Examples

### API Endpoints

After starting the server (`uvicorn app.main:app --reload`):

#### Chat with AI
```bash
POST /api/v1/chatbot/chat
{
    "message": "Which credit card is best for Myntra purchases?",
    "conversation_id": null
}
```

#### Search Knowledge Base
```bash
POST /api/v1/chatbot/search
{
    "query": "HDFC Regalia benefits",
    "limit": 5
}
```

#### Get Conversations
```bash
GET /api/v1/chatbot/conversations
```

### Python API Usage

```python
from app.core.ai_service import ai_service

# Process a user query
response = await ai_service.process_user_query(
    user_id=1,
    query="What are the best cashback credit cards?",
    conversation_id=None,
    db=None
)

print(response["response"])
```

## 🛠️ Maintenance Commands

### Update Documents
```bash
# Re-process all documents
python -m app.scripts.setup_complete_knowledge_base --force-reingest

# Process only new documents
python -m app.scripts.setup_complete_knowledge_base --skip-processing
```

### Database Management
```bash
# Check ChromaDB status
python -c "from app.core.vector_db import vector_db_service; print(vector_db_service.get_database_info())"

# Clean up old documents
python -m app.scripts.ingest_to_chroma --cleanup-days 30
```

### Monitoring
```bash
# Health check
curl http://localhost:8000/api/v1/chatbot/health

# System test
python -m app.scripts.test_system --quick
```

## 🔍 Troubleshooting

### Common Issues

#### 1. No documents in ChromaDB
```bash
# Check if processing worked
ls app/data/documents/chunks/

# Re-run setup
python -m app.scripts.setup_complete_knowledge_base --force-reingest
```

#### 2. Vector search returns no results
```bash
# Test vector database directly
python -m app.scripts.test_system --interactive
```

#### 3. Web scraping fails
- Check if URLs are accessible
- Some sites may require JavaScript (set `javascript_required: true`)
- Update selectors in configuration

#### 4. PDF processing fails
- Ensure PDFs are accessible and not password-protected
- Check file format (some PDFs may not be text-extractable)

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Optimization

### ChromaDB Optimization
```python
# Adjust collection settings for better performance
collection_metadata = {
    "hnsw:space": "cosine",
    "hnsw:construction_ef": 200,  # Higher = better recall, slower indexing
    "hnsw:search_ef": 100,        # Higher = better recall, slower search
    "hnsw:M": 16                  # Higher = better recall, more memory
}
```

### Caching
- Redis caching is configured for frequent queries
- Vector search results are cached for 1 hour

### Scaling Considerations
- For production: Consider migrating to Pinecone or Weaviate
- Current setup handles ~10K documents efficiently
- For larger datasets, implement batch processing

## 🚀 Deployment

### Production Setup
1. Set proper environment variables
2. Use PostgreSQL instead of SQLite
3. Configure Redis for caching
4. Set up proper logging
5. Use HTTPS and proper authentication

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Environment Variables for Production
```env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://redis:6379
OPENAI_API_KEY=your-key
SECRET_KEY=your-secret-key
```

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Update configuration examples
4. Document any new features

## 📞 Support

- Check the test system output for diagnostics
- Review logs in the console output
- Ensure all dependencies are properly installed
- Verify OpenAI API key is valid and has credits

---

## 🎯 Next Steps After Setup

1. **Test the API**: Visit `http://localhost:8000/docs`
2. **Add more credit cards**: Edit `document_sources.yaml`
3. **Customize responses**: Modify AI service prompts
4. **Integrate with frontend**: Use the chatbot API endpoints
5. **Monitor usage**: Set up logging and analytics

Happy building! 🚀 