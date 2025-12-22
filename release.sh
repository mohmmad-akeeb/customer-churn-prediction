#!/bin/bash

# Release Script for Customer Churn Prediction App
# Creates a Git tag for version v1.0.0

VERSION="v1.0.0"
RELEASE_MESSAGE="Release v1.0.0 - Customer Churn Prediction App

Features:
- FastAPI backend with Random Forest ML model
- Modern dark-themed responsive UI
- Real-time churn prediction with probability scores
- Docker support for easy deployment
- Comprehensive API documentation
- Health check endpoints
- Multiple deployment options (Render, Railway, Fly.io)

Tech Stack:
- FastAPI 0.104.1
- scikit-learn 1.5.2 (Random Forest)
- Python 3.11
- Docker support
- Uvicorn server

Model Performance:
- Provides probability estimates (not binary predictions)
- 2.3MB model size
- Fast predictions (<100ms)
"

echo "🚀 Release Script for Customer Churn Prediction"
echo "================================================"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Error: Git repository not initialized"
    echo "Run: git init"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo ""
    git status --short
    echo ""
    read -p "Do you want to commit these changes? (y/n): " commit_changes
    
    if [ "$commit_changes" = "y" ]; then
        echo ""
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
        echo "✅ Changes committed"
    else
        echo "❌ Please commit or stash your changes before creating a release"
        exit 1
    fi
fi

echo ""
echo "📝 Creating release $VERSION"
echo ""

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "⚠️  Tag $VERSION already exists"
    read -p "Do you want to delete and recreate it? (y/n): " recreate
    
    if [ "$recreate" = "y" ]; then
        git tag -d "$VERSION"
        git push origin :refs/tags/"$VERSION" 2>/dev/null
        echo "✅ Old tag deleted"
    else
        echo "❌ Aborted"
        exit 1
    fi
fi

# Create annotated tag
git tag -a "$VERSION" -m "$RELEASE_MESSAGE"

echo "✅ Tag $VERSION created locally"
echo ""

# Show tag info
echo "📋 Tag Information:"
git show "$VERSION" --no-patch
echo ""

# Ask to push
read -p "Do you want to push this tag to remote? (y/n): " push_tag

if [ "$push_tag" = "y" ]; then
    # Check if remote exists
    if git remote | grep -q origin; then
        git push origin "$VERSION"
        echo "✅ Tag pushed to remote"
        echo ""
        echo "🎉 Release $VERSION complete!"
        echo ""
        echo "Next steps:"
        echo "1. Create a GitHub release at: https://github.com/yourusername/churn-prediction/releases/new?tag=$VERSION"
        echo "2. Build and push Docker image:"
        echo "   docker build -t yourusername/churn-prediction:$VERSION ."
        echo "   docker push yourusername/churn-prediction:$VERSION"
        echo "3. Deploy to your hosting platform"
    else
        echo "⚠️  No remote repository configured"
        echo "Add remote with: git remote add origin <repository-url>"
        echo "Then push tag with: git push origin $VERSION"
    fi
else
    echo "✅ Tag created locally only"
    echo "Push later with: git push origin $VERSION"
fi

echo ""
echo "📦 To build Docker image with this version:"
echo "   docker build -t customer-churn-prediction:$VERSION ."
echo ""
echo "🏷️  To list all tags:"
echo "   git tag -l"
echo ""
echo "🗑️  To delete this tag:"
echo "   git tag -d $VERSION"
echo "   git push origin :refs/tags/$VERSION"
