#!/bin/bash

# Simple start script for local testing (without Docker)

echo "Starting The Admin Panel That Isn't..."
echo "========================================"

# Check if FLAG is set
if [ -z "$FLAG" ]; then
    echo "⚠️  WARNING: FLAG environment variable not set"
    echo "Setting default flag for testing..."
    export FLAG="flag{test_flag_for_local_development}"
fi

# Check if Redis is available
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  WARNING: Redis not found. Rate limiting will not work."
    echo "Install Redis: https://redis.io/download"
fi

# Check if Python dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Set environment variables
export REDIS_URL="${REDIS_URL:-redis://localhost:6379}"
export PORT="${PORT:-5000}"

echo ""
echo "Configuration:"
echo "  FLAG: ${FLAG:0:20}..."
echo "  REDIS_URL: $REDIS_URL"
echo "  PORT: $PORT"
echo ""
echo "Starting server..."
echo "Access at: http://localhost:$PORT"
echo ""

# Start the application
python3 -c "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=$PORT, debug=False)"
