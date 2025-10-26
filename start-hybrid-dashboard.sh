#!/bin/bash

# Hybrid Crypto Trading Bot Dashboard Startup Script
# Runs both Clojure crypto system and Python FastAPI backend

echo "🚀 Starting Hybrid Crypto Trading Bot Dashboard..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}Port $1 is already in use${NC}"
        return 1
    else
        echo -e "${GREEN}Port $1 is available${NC}"
        return 0
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=0
    
    echo -e "${YELLOW}Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}$service_name is ready!${NC}"
            return 0
        fi
        
        attempt=$((attempt + 1))
        echo -e "${YELLOW}Attempt $attempt/$max_attempts - waiting for $service_name...${NC}"
        sleep 2
    done
    
    echo -e "${RED}$service_name failed to start within expected time${NC}"
    return 1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${RED}Redis is not running. Please start Redis first.${NC}"
    echo "On macOS: brew services start redis"
    echo "On Ubuntu: sudo systemctl start redis"
    exit 1
fi
echo -e "${GREEN}✓ Redis is running${NC}"

# Check if ports are available
check_port 8080 || exit 1  # Clojure API
check_port 8000 || exit 1  # Python FastAPI
check_port 3000 || exit 1  # React frontend

# Check if Java is available
if ! command -v java &> /dev/null; then
    echo -e "${RED}Java is not installed. Please install Java 8+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Java is available${NC}"

# Check if Leiningen is available
if ! command -v lein &> /dev/null; then
    echo -e "${RED}Leiningen is not installed. Please install Leiningen first.${NC}"
    echo "Visit: https://leiningen.org/"
    exit 1
fi
echo -e "${GREEN}✓ Leiningen is available${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 is available${NC}"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install Node.js 16+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js is available${NC}"

echo -e "${BLUE}All prerequisites met!${NC}"

# Start Clojure HTTP API Server
echo -e "${BLUE}Starting Clojure HTTP API Server...${NC}"
cd crypto
lein run -m crypto.api.http/start-api-server! &
CLOJURE_PID=$!
cd ..

# Wait for Clojure API to be ready
wait_for_service "http://localhost:8080/health" "Clojure API"

# Start Python FastAPI Backend
echo -e "${BLUE}Starting Python FastAPI Backend...${NC}"
cd crypto-bot-mvp/backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
PYTHON_PID=$!
cd ../..

# Wait for Python API to be ready
wait_for_service "http://localhost:8000/" "Python FastAPI"

# Start React Frontend
echo -e "${BLUE}Starting React Frontend...${NC}"
cd crypto-bot-mvp/frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
    npm install
fi

# Start React development server
npm start &
REACT_PID=$!
cd ../..

# Wait for React frontend to be ready
wait_for_service "http://localhost:3000" "React Frontend"

echo -e "${GREEN}🎉 All services started successfully!${NC}"
echo ""
echo -e "${BLUE}Service URLs:${NC}"
echo -e "  Clojure API:     ${GREEN}http://localhost:8080${NC}"
echo -e "  Python FastAPI:  ${GREEN}http://localhost:8000${NC}"
echo -e "  React Frontend:  ${GREEN}http://localhost:3000${NC}"
echo -e "  API Documentation: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}Process IDs:${NC}"
echo -e "  Clojure API:     ${YELLOW}$CLOJURE_PID${NC}"
echo -e "  Python FastAPI:  ${YELLOW}$PYTHON_PID${NC}"
echo -e "  React Frontend:  ${YELLOW}$REACT_PID${NC}"
echo ""
echo -e "${YELLOW}To stop all services, press Ctrl+C or run:${NC}"
echo -e "  kill $CLOJURE_PID $PYTHON_PID $REACT_PID"
echo ""

# Function to cleanup on exit
cleanup() {
    echo -e "${YELLOW}Shutting down services...${NC}"
    kill $CLOJURE_PID $PYTHON_PID $REACT_PID 2>/dev/null
    echo -e "${GREEN}All services stopped.${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
echo -e "${BLUE}Press Ctrl+C to stop all services${NC}"
wait
