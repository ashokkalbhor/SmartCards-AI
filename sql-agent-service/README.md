# SQL Agent Service

An independent, containerized SQL agent service that provides natural language querying capabilities for credit card databases. Built with FastAPI, LangChain, OpenAI GPT-4, and ChromaDB.

## Features

- **Natural Language SQL Queries**: Convert natural language to SQL using OpenAI GPT-4
- **Independent Authentication**: JWT-based authentication system
- **Persistent Chat History**: Store and retrieve conversation history
- **Vector Database Integration**: ChromaDB for document embeddings
- **Configurable Database Schema**: Support for multiple database types
- **Containerized Deployment**: Ready for multi-project deployment
- **Real-time Document Processing**: Automatic vector database updates

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main API      │    │  SQL Agent      │    │   Vector DB     │
│   (Port 8000)   │◄──►│   Service       │◄──►│   (ChromaDB)    │
│                 │    │  (Port 8001)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   SQLite DB     │
                       │ (Chat History)  │
                       └─────────────────┘
```

## Quick Start

### 1. Environment Setup

Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=sqlite:///./smartcards_ai.db
ASYNC_DATABASE_URL=sqlite+aiosqlite:///./smartcards_ai.db
CHROMA_DB_PATH=./chroma_db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Service

```bash
python -m app.main
```

The service will be available at `http://localhost:8001`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout user

### Chat & Conversations

- `POST /api/v1/chat/conversations` - Create new conversation
- `GET /api/v1/chat/conversations` - Get user conversations
- `GET /api/v1/chat/conversations/{id}/history` - Get chat history
- `DELETE /api/v1/chat/conversations/{id}` - Delete conversation
- `POST /api/v1/chat/chat` - Chat with SQL agent
- `GET /api/v1/chat/stats` - Get chat statistics

### SQL Agent

- `POST /api/v1/sql-agent/query` - Process natural language query
- `GET /api/v1/sql-agent/health` - Health check
- `GET /api/v1/sql-agent/stats` - Service statistics

## Usage Examples

### 1. Register and Login

```bash
# Register
curl -X POST "http://localhost:8001/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# Login
curl -X POST "http://localhost:8001/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### 2. Chat with SQL Agent

```bash
# Start a conversation
curl -X POST "http://localhost:8001/api/v1/chat/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Which is the best credit card for Airtel spends?",
    "context": {"user_cards": ["HDFC Regalia", "ICICI Amazon Pay"]}
  }'
```

### 3. Get Chat History

```bash
# Get conversations
curl -X GET "http://localhost:8001/api/v1/chat/conversations" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get chat history
curl -X GET "http://localhost:8001/api/v1/chat/conversations/{conversation_id}/history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Docker Deployment

### Build Image

```bash
docker build -t sql-agent-service .
```

### Run Container

```bash
docker run -p 8001:8001 \
  -e OPENAI_API_KEY=your-key \
  -e DATABASE_URL=sqlite:///./smartcards_ai.db \
  -e JWT_SECRET_KEY=your-secret \
  -v $(pwd)/data:/app/data \
  sql-agent-service
```

### Multi-Project Deployment

For deploying to multiple projects with different databases:

```bash
# Project A
docker run -p 8001:8001 \
  -e OPENAI_API_KEY=your-key \
  -e DATABASE_URL=sqlite:///./data/project_a.db \
  -e JWT_SECRET_KEY=project_a_secret \
  -e CLIENT_ID=project_a \
  -v $(pwd)/data/project_a:/app/data \
  sql-agent-service

# Project B
docker run -p 8002:8001 \
  -e OPENAI_API_KEY=your-key \
  -e DATABASE_URL=sqlite:///./data/project_b.db \
  -e JWT_SECRET_KEY=project_b_secret \
  -e CLIENT_ID=project_b \
  -v $(pwd)/data/project_b:/app/data \
  sql-agent-service
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `DATABASE_URL` | Main database URL | `sqlite:///./smartcards_ai.db` |
| `ASYNC_DATABASE_URL` | Async database URL | `sqlite+aiosqlite:///./smartcards_ai.db` |
| `CHROMA_DB_PATH` | Vector database path | `./chroma_db` |
| `JWT_SECRET_KEY` | JWT secret key | Auto-generated |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |
| `CHAT_HISTORY_RETENTION_DAYS` | Chat retention | `90` |
| `SQL_AGENT_TABLES` | Accessible tables | All tables |

### Database Schema Configuration

The service automatically introspects the database schema. To limit access to specific tables:

```env
SQL_AGENT_TABLES=credit_cards,card_master_data,merchants,transactions
```

## Development

### Project Structure

```
sql-agent-service/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── chat.py          # Chat endpoints
│   │   └── queries.py       # SQL agent endpoints
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database models
│   │   ├── security.py      # JWT authentication
│   │   └── sql_agent.py     # SQL agent service
│   ├── models/
│   │   ├── chat_models.py   # Chat Pydantic models
│   │   └── query_models.py  # Query Pydantic models
│   ├── services/
│   │   ├── chat_service.py  # Chat history service
│   │   ├── cache_service.py # Caching service
│   │   └── vector_service.py # Vector DB service
│   └── main.py              # FastAPI application
├── requirements.txt
├── Dockerfile
└── README.md
```

### Running Tests

```bash
pytest tests/
```

### Database Migrations

```bash
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

## Integration with Main API

The main API can communicate with this service via HTTP:

```python
import httpx

async def query_sql_agent(query: str, user_context: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/api/v1/sql-agent/query",
            json={"query": query, "user_context": user_context},
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt password hashing
- **CORS Protection**: Configurable CORS settings
- **Rate Limiting**: Built-in rate limiting
- **Input Validation**: Pydantic model validation
- **SQL Injection Protection**: Parameterized queries

## Monitoring & Health Checks

- **Health Endpoint**: `/health` for service status
- **Statistics**: `/api/v1/sql-agent/stats` for usage metrics
- **Logging**: Comprehensive logging with configurable levels
- **Error Handling**: Global exception handling

## Performance Optimization

- **Caching**: In-memory caching for query results
- **Connection Pooling**: Database connection pooling
- **Async Operations**: Full async/await support
- **Vector Search**: Efficient similarity search
- **Query Optimization**: SQL query optimization hints

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Check `DATABASE_URL` and file permissions
2. **OpenAI API Error**: Verify `OPENAI_API_KEY` is valid
3. **JWT Token Error**: Check `JWT_SECRET_KEY` configuration
4. **Vector DB Error**: Ensure `CHROMA_DB_PATH` is writable

### Logs

Check logs for detailed error information:

```bash
docker logs sql-agent-service
```

## License

This project is licensed under the MIT License.
