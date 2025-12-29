#!/bin/bash

# ConsensusWatch Deployment Script
# Quick deployment to various platforms

set -e

echo "🤖 ConsensusWatch Deployment Helper"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}Checking prerequisites...${NC}"

    if ! command_exists git; then
        echo -e "${RED}❌ Git is not installed${NC}"
        exit 1
    fi

    if ! command_exists docker; then
        echo -e "${YELLOW}⚠️  Docker is not installed (optional for local testing)${NC}"
    else
        echo -e "${GREEN}✅ Docker installed${NC}"
    fi

    echo ""
}

# Test locally with Docker
test_local() {
    echo -e "${BLUE}🧪 Testing locally with Docker...${NC}"

    if ! command_exists docker; then
        echo -e "${RED}❌ Docker is required for local testing${NC}"
        exit 1
    fi

    if ! command_exists docker-compose; then
        echo -e "${RED}❌ docker-compose is required${NC}"
        exit 1
    fi

    echo "Building and starting services..."
    docker-compose up --build -d

    echo ""
    echo -e "${GREEN}✅ Application started!${NC}"
    echo -e "   Web Dashboard: ${BLUE}http://localhost:8501${NC}"
    echo -e "   API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "   Redis: ${BLUE}localhost:6379${NC}"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
}

# Deploy to Streamlit Cloud
deploy_streamlit() {
    echo -e "${BLUE}☁️  Deploying to Streamlit Cloud...${NC}"
    echo ""
    echo "Steps:"
    echo "1. Push your code to GitHub"
    echo "2. Go to https://share.streamlit.io"
    echo "3. Connect your GitHub repository"
    echo "4. Set main file: dashboard/app_new.py"
    echo "5. Add secrets (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)"
    echo "6. Click Deploy"
    echo ""
    echo -e "${GREEN}✅ Follow the steps above to deploy${NC}"
}

# Deploy to Railway
deploy_railway() {
    echo -e "${BLUE}🚂 Deploying to Railway...${NC}"

    if ! command_exists railway; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi

    echo "Logging in to Railway..."
    railway login

    echo "Initializing project..."
    railway init

    echo "Adding environment variables..."
    echo "Please enter your Reddit API credentials:"
    read -p "REDDIT_CLIENT_ID: " client_id
    read -sp "REDDIT_CLIENT_SECRET: " client_secret
    echo ""

    railway variables set REDDIT_CLIENT_ID="$client_id"
    railway variables set REDDIT_CLIENT_SECRET="$client_secret"
    railway variables set REDDIT_USER_AGENT="ConsensusWatch/0.1.0"

    echo "Deploying..."
    railway up

    echo ""
    echo -e "${GREEN}✅ Deployed to Railway!${NC}"
    echo "Run 'railway open' to view your deployment"
}

# Deploy to Heroku
deploy_heroku() {
    echo -e "${BLUE}🟣 Deploying to Heroku...${NC}"

    if ! command_exists heroku; then
        echo -e "${RED}❌ Heroku CLI is not installed${NC}"
        echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi

    echo "Logging in to Heroku..."
    heroku login

    echo "Creating Heroku app..."
    heroku create consensuswatch-$(date +%s)

    echo "Adding Redis addon..."
    heroku addons:create heroku-redis:mini

    echo "Setting environment variables..."
    read -p "REDDIT_CLIENT_ID: " client_id
    read -sp "REDDIT_CLIENT_SECRET: " client_secret
    echo ""

    heroku config:set REDDIT_CLIENT_ID="$client_id"
    heroku config:set REDDIT_CLIENT_SECRET="$client_secret"
    heroku config:set REDDIT_USER_AGENT="ConsensusWatch/0.1.0"

    echo "Deploying..."
    git push heroku main

    echo ""
    echo -e "${GREEN}✅ Deployed to Heroku!${NC}"
    echo "Run 'heroku open' to view your app"
}

# Deploy to DigitalOcean
deploy_digitalocean() {
    echo -e "${BLUE}🌊 Deploying to DigitalOcean App Platform...${NC}"

    if ! command_exists doctl; then
        echo -e "${YELLOW}⚠️  DigitalOcean CLI (doctl) not installed${NC}"
        echo "Install from: https://docs.digitalocean.com/reference/doctl/how-to/install/"
        echo ""
        echo "Or deploy manually:"
        echo "1. Go to https://cloud.digitalocean.com/apps"
        echo "2. Click 'Create App'"
        echo "3. Connect your GitHub repository"
        echo "4. Use the .do/app.yaml configuration"
        exit 1
    fi

    echo "Deploying..."
    doctl apps create --spec .do/app.yaml

    echo -e "${GREEN}✅ Deployment initiated!${NC}"
}

# Main menu
show_menu() {
    echo "Select deployment option:"
    echo "1) Test locally with Docker"
    echo "2) Deploy to Streamlit Cloud (FREE)"
    echo "3) Deploy to Railway"
    echo "4) Deploy to Heroku"
    echo "5) Deploy to DigitalOcean"
    echo "6) Show deployment documentation"
    echo "0) Exit"
    echo ""
    read -p "Enter choice [0-6]: " choice

    case $choice in
        1) test_local ;;
        2) deploy_streamlit ;;
        3) deploy_railway ;;
        4) deploy_heroku ;;
        5) deploy_digitalocean ;;
        6) cat DEPLOYMENT.md ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}"; show_menu ;;
    esac
}

# Main execution
check_prerequisites
show_menu
