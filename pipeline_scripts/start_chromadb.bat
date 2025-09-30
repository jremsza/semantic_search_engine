@echo off
REM Simple script to start only ChromaDB in Docker

echo 🚀 Starting ChromaDB server...

REM Create data directory if it doesn't exist
if not exist "data\chroma" mkdir data\chroma

REM Start ChromaDB using the simple compose file
docker-compose -f docker-compose.simple.yml up -d

REM Wait for ChromaDB to be ready
echo ⏳ Waiting for ChromaDB to be ready...
timeout /t 10 /nobreak > nul

REM Check if ChromaDB is running
echo 🔍 Checking ChromaDB status...
curl -f http://localhost:8000/api/v1/heartbeat > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ChromaDB is running successfully!
    echo 🌐 ChromaDB API available at: http://localhost:8000
    echo 📊 ChromaDB Admin UI available at: http://localhost:8000/admin
    echo.
    echo 💡 You can now connect from your local Python scripts using:
    echo    client = chromadb.HttpClient(host="localhost", port=8000)
) else (
    echo ❌ ChromaDB failed to start. Check logs with:
    echo    docker-compose -f docker-compose.simple.yml logs
)

echo.
echo 📋 Management commands:
echo   📊 View logs: docker-compose -f docker-compose.simple.yml logs -f
echo   🛑 Stop ChromaDB: docker-compose -f docker-compose.simple.yml down
echo   🔄 Restart: docker-compose -f docker-compose.simple.yml restart
pause
