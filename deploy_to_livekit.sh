#!/bin/bash

# Deploy LiveKit Agent to LiveKit Cloud
# This script automates the deployment process

set -e  # Exit on error

echo "🚀 LiveKit Agent Deployment Script"
echo "===================================="
echo ""

# Check if lk CLI is installed
if ! command -v lk &> /dev/null; then
    echo "❌ LiveKit CLI (lk) is not installed"
    echo "Install it with: brew install livekit"
    exit 1
fi

echo "✅ LiveKit CLI found: $(lk --version)"
echo ""

# Check if user is authenticated
echo "📋 Step 1: Authenticate with LiveKit Cloud"
echo "Running: lk cloud auth"
echo ""
lk cloud auth

echo ""
echo "📋 Step 2: List available projects"
echo "Running: lk project list"
echo ""
lk project list

echo ""
echo "📋 Step 3: Create agent (if not already created)"
echo ""
read -p "Enter your region (us-west, us-east, eu-central, ap-southeast) [default: us-west]: " REGION
REGION=${REGION:-us-west}

read -p "Enter your OpenAI API key: " OPENAI_KEY

if [ -z "$OPENAI_KEY" ]; then
    echo "❌ OpenAI API key is required"
    exit 1
fi

echo ""
echo "Creating agent with region: $REGION"
lk agent create --region "$REGION" --secrets OPENAI_API_KEY="$OPENAI_KEY"

echo ""
echo "📋 Step 4: Deploy agent to LiveKit Cloud"
echo "Running: lk agent deploy"
echo ""
lk agent deploy

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Next steps:"
echo "  1. Monitor logs: lk agent logs --follow"
echo "  2. Check status: lk agent list"
echo "  3. View dashboard: https://cloud.livekit.io"
echo ""
echo "🎉 Your agent is now live and running on LiveKit Cloud!"
