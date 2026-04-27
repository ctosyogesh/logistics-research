#!/bin/bash

# Logistics Research Agent - Startup Script
# This script starts both backend and frontend servers

echo "🚀 Starting Logistics Research Agent..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Error: backend/.env file not found${NC}"
    echo "Please copy backend/.env.example to backend/.env and add your API key"
    echo ""
    echo "Run: cp backend/.env.example backend/.env"
    echo "Then edit backend/.env and add your ANTHROPIC_API_KEY"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    cd frontend && npm install && cd ..
fi

# Start backend in background
echo -e "${GREEN}🔧 Starting Backend Server (Port 8000)...${NC}"
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo -e "${GREEN}🎨 Starting Frontend Server (Port 3000)...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✅ Application Started Successfully!${NC}"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit 0
}

# Set trap to catch Ctrl+C
trap cleanup INT

# Wait for processes
wait
