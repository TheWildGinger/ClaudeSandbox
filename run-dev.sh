#!/bin/bash

# EngiCalc Development Server Launcher
# This script starts both backend and frontend servers

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  EngiCalc Development Server${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}Error: Poetry is not installed${NC}"
    echo "Install it with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Install it from: https://nodejs.org/"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo -e "\n${RED}Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if backend dependencies are installed
if [ ! -d "backend/.venv" ]; then
    echo -e "${BLUE}Installing backend dependencies...${NC}"
    cd backend
    poetry install
    cd ..
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Start backend server
echo -e "${GREEN}Starting backend server...${NC}"
cd backend
poetry run python -m app.main &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend server
echo -e "${GREEN}Starting frontend server...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  EngiCalc is running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Backend:  ${BLUE}http://localhost:8000${NC}"
echo -e "Frontend: ${BLUE}http://localhost:5173${NC}"
echo -e "API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop both servers${NC}"
echo ""

# Wait for either process to exit
wait $BACKEND_PID $FRONTEND_PID
