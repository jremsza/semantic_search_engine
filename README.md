# Semantic Search System

A web-based semantic search engine for data science knowledge base.

## Quick Start

### 1. Start ChromaDB
**Command Prompt/PowerShell:**
```bash
docker-compose up -d
```

**PowerShell (alternative):**
```powershell
docker-compose up -d
```

### 2. Launch Web App
**Command Prompt:**
```bash
streamlit run src/search_engine.py
```

**PowerShell:**
```powershell
streamlit run src/search_engine.py
```

### 3. Open Your Browser
Go to `http://localhost:8501`

## How to Use

1. **Type your question** in the search box (e.g., "What is a transformer?")
2. **Click Search** to find relevant documents
3. **View results** with similarity scores and expandable content

## Features

- ✅ **6,579 documents** from data science topics
- ✅ **Semantic search** using embeddings
- ✅ **Similarity scores** to show relevance
- ✅ **Web interface** - no coding required
- ✅ **Real-time results** as you type

## Architecture

```
Streamlit Web App → ChromaDB (Docker)
```

