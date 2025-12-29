#!/bin/bash

# Complete Deployment Script for Vercel + Streamlit Cloud
# This script guides you through the entire deployment process

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${PURPLE}"
cat << "EOF"
   ____                                        _    _       _       _
  / ___|___  _ __  ___  ___ _ __  ___ _   _ __| |  | | __ _| |_ ___| |__
 | |   / _ \| '_ \/ __|/ _ \ '_ \/ __| | | / _` |  | |/ _` | __/ __| '_ \
 | |__| (_) | | | \__ \  __/ | | \__ \ |_| \__,_|  | | (_| | || (__| | | |
  \____\___/|_| |_|___/\___|_| |_|___/\__,_|   |___|_|\__,_|\__\___|_| |_|
                                                  |_____|
EOF
echo -e "${NC}"
echo -e "${CYAN}Complete Deployment Guide${NC}"
echo "========================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for user
wait_for_user() {
    echo ""
    read -p "Press Enter to continue..."
    echo ""
}

# Step 1: Reddit Account Setup
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}STEP 1: Reddit API Credentials${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "First, we need Reddit API credentials."
echo ""
echo "Option 1: Create new Reddit account for the app"
echo "  → https://www.reddit.com/register"
echo "  → Username: ConsensusWatchBot (or similar)"
echo ""
echo "Option 2: Use existing Reddit account"
echo "  → Just use your current account"
echo ""
wait_for_user

echo "Now, create a Reddit app to get credentials:"
echo ""
echo -e "${YELLOW}1. Visit: https://www.reddit.com/prefs/apps${NC}"
echo -e "${YELLOW}2. Scroll down and click 'create another app...'${NC}"
echo -e "${YELLOW}3. Fill in:${NC}"
echo "   - Name: ConsensusWatch"
echo "   - Type: script (SELECT THIS!)"
echo "   - Description: Bot detection tool"
echo "   - Redirect URI: http://localhost:8501"
echo -e "${YELLOW}4. Click 'create app'${NC}"
echo ""
echo "Opening Reddit apps page in browser..."
sleep 2

# Try to open browser
if command_exists xdg-open; then
    xdg-open "https://www.reddit.com/prefs/apps" 2>/dev/null
elif command_exists open; then
    open "https://www.reddit.com/prefs/apps" 2>/dev/null
fi

wait_for_user

echo "After creating the app, you'll see:"
echo ""
echo "  ConsensusWatch"
echo "  personal use script"
echo "  "
echo "  ABCdef123GHI456           ← CLIENT_ID (under app name)"
echo "  "
echo "  secret: jklMNO789pqrSTU   ← CLIENT_SECRET"
echo ""

# Collect credentials
echo -e "${GREEN}Enter your Reddit API credentials:${NC}"
echo ""
read -p "REDDIT_CLIENT_ID: " REDDIT_CLIENT_ID
read -p "REDDIT_CLIENT_SECRET: " REDDIT_CLIENT_SECRET

if [ -z "$REDDIT_CLIENT_ID" ] || [ -z "$REDDIT_CLIENT_SECRET" ]; then
    echo -e "${RED}Error: Credentials cannot be empty!${NC}"
    exit 1
fi

REDDIT_USER_AGENT="ConsensusWatch/0.1.0"

echo ""
echo -e "${GREEN}✓ Credentials collected!${NC}"
echo ""

# Save to .env file
echo "Saving to .env file..."
cat > .env << EOF
# Reddit API Credentials
REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET=$REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT=$REDDIT_USER_AGENT
EOF

echo -e "${GREEN}✓ Saved to .env file${NC}"
wait_for_user

# Step 2: Vercel Setup
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}STEP 2: Deploy API to Vercel${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check for Vercel CLI
if ! command_exists vercel; then
    echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"

    if command_exists npm; then
        npm install -g vercel
    else
        echo -e "${RED}npm not found. Please install Node.js first:${NC}"
        echo "https://nodejs.org/"
        exit 1
    fi
fi

echo -e "${GREEN}✓ Vercel CLI ready${NC}"
echo ""

# Login to Vercel
echo "Logging in to Vercel..."
echo "(Browser will open for authentication)"
sleep 2
vercel login

echo ""
echo -e "${GREEN}✓ Logged in to Vercel${NC}"
echo ""

# Add environment variables
echo "Adding environment variables to Vercel..."
echo ""
echo "$REDDIT_CLIENT_ID" | vercel env add REDDIT_CLIENT_ID production
echo "$REDDIT_CLIENT_SECRET" | vercel env add REDDIT_CLIENT_SECRET production
echo "$REDDIT_USER_AGENT" | vercel env add REDDIT_USER_AGENT production

echo ""
echo -e "${GREEN}✓ Environment variables added${NC}"
wait_for_user

# Deploy to Vercel
echo "Deploying API to Vercel..."
echo ""
vercel --prod

echo ""
echo -e "${GREEN}✓ API deployed to Vercel!${NC}"
echo ""
echo "Your API is live! Test it:"
echo -e "${CYAN}curl https://consensuswatch-api.vercel.app/api/v1/health${NC}"
echo ""
wait_for_user

# Step 3: Streamlit Cloud
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}STEP 3: Deploy Dashboard to Streamlit Cloud${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check git status
if ! command_exists git; then
    echo -e "${RED}Git not found. Please install git first.${NC}"
    exit 1
fi

echo "Checking git status..."
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}Uncommitted changes found. Committing...${NC}"
    git add -A
    git commit -m "Ready for deployment"
fi

echo "Pushing to GitHub..."
git push origin $(git branch --show-current)

echo ""
echo -e "${GREEN}✓ Code pushed to GitHub${NC}"
echo ""

echo "Now, let's deploy to Streamlit Cloud:"
echo ""
echo -e "${YELLOW}1. Visit: https://share.streamlit.io${NC}"
echo -e "${YELLOW}2. Sign in with GitHub${NC}"
echo -e "${YELLOW}3. Click 'New app'${NC}"
echo -e "${YELLOW}4. Configure:${NC}"
echo "   - Repository: $(git remote get-url origin)"
echo "   - Branch: $(git branch --show-current)"
echo "   - Main file: dashboard/app_new.py"
echo ""
echo -e "${YELLOW}5. Click 'Advanced settings'${NC}"
echo -e "${YELLOW}6. In 'Secrets', paste this:${NC}"
echo ""
echo -e "${CYAN}─────────────────────────────────────${NC}"
cat << EOF
REDDIT_CLIENT_ID = "$REDDIT_CLIENT_ID"
REDDIT_CLIENT_SECRET = "$REDDIT_CLIENT_SECRET"
REDDIT_USER_AGENT = "$REDDIT_USER_AGENT"
EOF
echo -e "${CYAN}─────────────────────────────────────${NC}"
echo ""
echo -e "${YELLOW}7. Click 'Deploy!'${NC}"
echo ""

echo "Opening Streamlit Cloud in browser..."
sleep 2

if command_exists xdg-open; then
    xdg-open "https://share.streamlit.io/deploy" 2>/dev/null
elif command_exists open; then
    open "https://share.streamlit.io/deploy" 2>/dev/null
fi

wait_for_user

# Step 4: Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETE!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Your ConsensusWatch app is now live!"
echo ""
echo -e "${CYAN}Your URLs:${NC}"
echo "  Dashboard: https://[your-app].streamlit.app"
echo "  API: https://consensuswatch-api.vercel.app"
echo "  API Docs: https://consensuswatch-api.vercel.app/docs"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "  1. Test your dashboard with a Reddit URL"
echo "  2. Share your app with others"
echo "  3. Monitor usage in Vercel/Streamlit dashboards"
echo "  4. Set up custom domain (optional)"
echo ""
echo -e "${GREEN}Need help? Check DEPLOYMENT_WALKTHROUGH.md${NC}"
echo ""
echo -e "${PURPLE}Thank you for using ConsensusWatch! 🤖${NC}"
echo ""
