#!/bin/bash
# Startup script for Railway deployment

echo "Starting CEDOS Backend..."

# Run migrations (with error handling)
echo "Running database migrations..."
alembic upgrade head || {
    echo "WARNING: Migration failed. This might be because:"
    echo "  1. Database URL not set correctly"
    echo "  2. Database not accessible"
    echo "  3. Migrations already applied"
    echo "Continuing with server start..."
}

# Start server
echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
