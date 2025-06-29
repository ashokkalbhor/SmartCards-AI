# SmartCards AI - Setup Guide

This guide will help you set up the SmartCards AI application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Docker & Docker Compose** (Recommended)
- **Python 3.9+** (for local development)
- **Node.js 18+** (for local development)
- **PostgreSQL** (for local development)
- **Redis** (for local development)

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SmartCards-AI
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
# Backend Environment Variables
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=postgresql://smartcards_user:smartcards_password@postgres:5432/smartcards_ai
ASYNC_DATABASE_URL=postgresql+asyncpg://smartcards_user:smartcards_password@postgres:5432/smartcards_ai
REDIS_URL=redis://redis:6379
ENVIRONMENT=development
DEBUG=true

# Frontend Environment Variables
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

### 3. Start the Application

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

## Local Development Setup

### Backend Setup

1. **Create Virtual Environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Environment Variables**

Create a `.env` file in the `backend` directory:

```bash
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_URL=postgresql://smartcards_user:smartcards_password@localhost:5432/smartcards_ai
ASYNC_DATABASE_URL=postgresql+asyncpg://smartcards_user:smartcards_password@localhost:5432/smartcards_ai
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
DEBUG=true
```

4. **Set Up Database**

```bash
# Create database
createdb smartcards_ai

# Run migrations (when available)
alembic upgrade head

# Or create tables directly
python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

5. **Start the Backend**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**

```bash
cd frontend
npm install
```

2. **Set Environment Variables**

Create a `.env` file in the `frontend` directory:

```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development
```

3. **Start the Frontend**

```bash
npm start
```

## Database Setup

### PostgreSQL Setup

1. **Install PostgreSQL**

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

2. **Create Database and User**

```sql
CREATE DATABASE smartcards_ai;
CREATE USER smartcards_user WITH PASSWORD 'smartcards_password';
GRANT ALL PRIVILEGES ON DATABASE smartcards_ai TO smartcards_user;
```

### Redis Setup

1. **Install Redis**

```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows
# Download from https://redis.io/download
```

2. **Start Redis**

```bash
redis-server
```

## API Documentation

Once the backend is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Production Deployment

### Environment Variables

For production, update the environment variables:

```bash
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-production-database-url
REDIS_URL=your-production-redis-url
```

### Docker Production

```bash
# Build and start production services
docker-compose --profile production up -d

# Or build individual services
docker-compose build backend frontend
docker-compose up -d postgres redis backend frontend nginx
```

### Manual Production Setup

1. **Backend Deployment**
   - Use a production WSGI server like Gunicorn
   - Set up reverse proxy with Nginx
   - Configure SSL certificates
   - Set up monitoring and logging

2. **Frontend Deployment**
   - Build the production bundle: `npm run build`
   - Serve static files with Nginx or CDN
   - Configure environment variables

3. **Database**
   - Use managed PostgreSQL service
   - Set up automated backups
   - Configure connection pooling

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check if PostgreSQL is running
   - Verify database credentials
   - Ensure database exists

2. **Redis Connection Error**
   - Check if Redis is running
   - Verify Redis URL configuration

3. **Frontend Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version compatibility

4. **Docker Issues**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild images: `docker-compose build --no-cache`

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

## Development Workflow

1. **Feature Development**
   - Create feature branch: `git checkout -b feature/your-feature`
   - Make changes and test locally
   - Commit changes: `git commit -m "Add feature"`
   - Push and create pull request

2. **Code Quality**
   - Run linting: `npm run lint` (frontend) / `flake8` (backend)
   - Run tests before committing
   - Follow code style guidelines

3. **Database Changes**
   - Create migration: `alembic revision --autogenerate -m "Description"`
   - Apply migration: `alembic upgrade head`
   - Test migration rollback

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the logs for error messages
3. Check the API documentation
4. Create an issue in the repository

## Contributing

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct and the process for submitting pull requests. 