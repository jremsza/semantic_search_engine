# ChromaDB Docker Setup for Semantic Search

This guide will help you set up ChromaDB in a Docker container while developing your semantic search project locally.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (usually included with Docker Desktop)
- Python 3.8+ installed on your local machine

## Quick Start

### Option 1: Using Setup Scripts (Recommended)

**For Windows:**
```bash
# Run the ChromaDB setup script
scripts\start_chromadb.bat
```

**For Linux/Mac:**
```bash
# Make script executable and run
chmod +x scripts/start_chromadb.sh
./scripts/start_chromadb.sh
```

### Option 2: Manual Setup

1. **Start ChromaDB:**
   ```bash
   docker-compose -f docker-compose.simple.yml up -d
   ```

2. **Check if ChromaDB is running:**
   ```bash
   docker-compose -f docker-compose.simple.yml ps
   ```

3. **View logs:**
   ```bash
   docker-compose -f docker-compose.simple.yml logs -f
   ```

## Local Development Setup

### Install Local Dependencies

```bash
# Install Python packages for local development
pip install -r requirements.local.txt
```

### Connect to ChromaDB from Your Local Python

```python
import chromadb

# Connect to ChromaDB server running in Docker
client = chromadb.HttpClient(
    host="localhost",
    port=8000
)

# Create or get a collection
collection = client.get_or_create_collection(
    name="semantic_search",
    metadata={"hnsw:space": "cosine"}
)

# Add documents
collection.add(
    documents=["Your document text here"],
    metadatas=[{"source": "example"}],
    ids=["doc1"]
)

# Query the collection
results = collection.query(
    query_texts=["search query"],
    n_results=5
)
```

## Architecture

This setup uses a **hybrid approach**:

```
Your Local Machine                    Docker Container
├── Your Python scripts              ├── ChromaDB Server
├── Your notebooks                   ├── Port 8000
├── Your data files                  └── Persistent data
└── ChromaDB Client                  └── ./data/chroma/
    └── Connects to localhost:8000
```

## Services

### ChromaDB Server
- **Port:** 8000
- **API Endpoint:** http://localhost:8000
- **Admin UI:** http://localhost:8000/admin
- **Health Check:** http://localhost:8000/api/v1/heartbeat
- **Data Storage:** `./data/chroma/` (persistent)

## Data Persistence

- ChromaDB data is persisted in `./data/chroma/`
- Your project data in `./data/` is accessible to both local and container
- Data survives container restarts and rebuilds

## Management Commands

### Start ChromaDB
```bash
# Using script (recommended)
scripts\start_chromadb.bat  # Windows
./scripts/start_chromadb.sh  # Linux/Mac

# Or manually
docker-compose -f docker-compose.simple.yml up -d
```

### View Logs
```bash
# All services
docker-compose -f docker-compose.simple.yml logs -f

# Specific service
docker-compose -f docker-compose.simple.yml logs chromadb
```

### Stop ChromaDB
```bash
docker-compose -f docker-compose.simple.yml down
```

### Restart ChromaDB
```bash
docker-compose -f docker-compose.simple.yml restart
```

### Clean Up (Remove all data)
```bash
# Stop and remove containers and data
docker-compose -f docker-compose.simple.yml down -v

# Clean up unused Docker resources
docker system prune -f
```

## Configuration

### Environment Variables

You can customize the setup by modifying the environment variables in `docker-compose.simple.yml`:

```yaml
environment:
  - CHROMA_SERVER_HOST=0.0.0.0
  - CHROMA_SERVER_HTTP_PORT=8000
  - CHROMA_SERVER_CORS_ALLOW_ORIGINS=["*"]
```

### Port Configuration

To change ports, modify the `ports` section in `docker-compose.simple.yml`:

```yaml
ports:
  - "8001:8000"  # Change 8001 to your preferred port
```

## Development Workflow

1. **Start ChromaDB:**
   ```bash
   scripts\start_chromadb.bat  # Windows
   ```

2. **Develop locally:**
   - Use your favorite IDE/editor
   - Run Python scripts locally
   - Work with Jupyter notebooks locally

3. **Connect to ChromaDB:**
   - Use `chromadb.HttpClient(host="localhost", port=8000)`
   - Access admin UI at http://localhost:8000/admin

4. **Stop when done:**
   ```bash
   docker-compose -f docker-compose.simple.yml down
   ```

## Troubleshooting

### ChromaDB Not Starting

1. **Check if port 8000 is available:**
   ```bash
   netstat -an | findstr :8000  # Windows
   lsof -i :8000  # Linux/Mac
   ```

2. **Check Docker logs:**
   ```bash
   docker-compose -f docker-compose.simple.yml logs chromadb
   ```

3. **Verify Docker is running:**
   ```bash
   docker --version
   docker-compose --version
   ```

### Permission Issues

If you encounter permission issues with data directories:

```bash
# Windows (run as Administrator)
icacls data /grant Everyone:F /T

# Linux/Mac
sudo chown -R $USER:$USER data/
```

### Connection Issues

If you can't connect from Python:

1. **Verify ChromaDB is running:**
   ```bash
   curl http://localhost:8000/api/v1/heartbeat
   ```

2. **Check firewall settings** - ensure port 8000 is not blocked

3. **Try connecting with curl:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/collections \
     -H "Content-Type: application/json" \
     -d '{"name": "test_collection"}'
   ```

## Benefits of This Setup

1. **Lightweight**: Only ChromaDB runs in Docker
2. **Local Development**: Use your favorite tools and IDE
3. **Easy Setup**: Uses official ChromaDB Docker image
4. **Data Persistence**: Your data survives container restarts
5. **Simple Management**: Easy to start/stop ChromaDB
6. **No Conflicts**: Your local Python environment stays clean

## Support

If you encounter issues:

1. Check the logs: `docker-compose -f docker-compose.simple.yml logs -f`
2. Verify your Docker installation
3. Ensure ports are not in use by other services
4. Check the ChromaDB documentation: https://docs.trychroma.com/