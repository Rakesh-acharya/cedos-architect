#!/bin/bash
# Quick Deploy Script for Railway

echo "============================================================"
echo "  CEDOS Backend - Railway Deployment"
echo "============================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Navigate to backend
cd backend || exit

echo "Step 1: Login to Railway..."
railway login

echo ""
echo "Step 2: Initialize Railway project..."
railway init

echo ""
echo "Step 3: Setting environment variables..."
echo "Please enter your Supabase password:"
read -s SUPABASE_PASSWORD

railway variables set DATABASE_URL="postgresql://postgres:${SUPABASE_PASSWORD}@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="$(openssl rand -hex 32)"
railway variables set BACKEND_CORS_ORIGINS='["*"]'

echo ""
echo "Step 4: Deploying to Railway..."
railway up

echo ""
echo "Step 5: Running migrations..."
railway run alembic upgrade head

echo ""
echo "Step 6: Creating default users..."
railway run python create_default_users.py

echo ""
echo "============================================================"
echo "  Deployment Complete!"
echo "============================================================"
echo ""
echo "Get your URL:"
railway domain
echo ""
echo "API Docs: https://your-url.up.railway.app/api/docs"
echo ""
