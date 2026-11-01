#!/bin/bash

# Customer Churn Prediction - Quick Deploy Script
# This script helps you deploy to GitHub quickly

echo "🚀 Customer Churn Prediction - Deployment Helper"
echo "================================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 Setting up GitHub remote..."
    echo "Please enter your GitHub repository URL:"
    echo "Example: https://github.com/username/churn-prediction.git"
    read -p "Repository URL: " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added: $repo_url"
    else
        echo "⚠️  No URL provided, skipping remote setup"
    fi
else
    echo "✅ Remote already configured"
fi

echo ""
echo "📝 Staging files..."
git add .

echo ""
echo "💬 Creating commit..."
git commit -m "Initial commit - Customer Churn Prediction App" || echo "⚠️  No changes to commit"

echo ""
echo "🌿 Checking branch..."
git branch -M main

echo ""
echo "📤 Ready to push to GitHub!"
echo ""
echo "Run this command to push:"
echo "  git push -u origin main"
echo ""
echo "Then deploy on:"
echo "  1. Render.com (Recommended): https://render.com"
echo "  2. Railway.app: https://railway.app"
echo "  3. Fly.io: https://fly.io"
echo ""
echo "✨ See DEPLOYMENT_SUMMARY.md for detailed instructions"
