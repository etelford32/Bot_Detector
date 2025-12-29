# 🚀 Quick Start Guide

Get ConsensusWatch up and running in 5 minutes!

## Option 1: Deploy to Streamlit Cloud (FREE & Easiest)

**Perfect for getting started quickly**

### Steps:

1. **Fork this repository** on GitHub

2. **Get Reddit API credentials:**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App"
   - Name: `ConsensusWatch`
   - Type: `script`
   - Redirect URI: `http://localhost:8501`
   - Copy your `client_id` and `client_secret`

3. **Deploy to Streamlit:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your forked repository
   - Main file: `dashboard/app_new.py`
   - Click "Advanced settings"
   - Add secrets:
     ```toml
     REDDIT_CLIENT_ID = "your_client_id_here"
     REDDIT_CLIENT_SECRET = "your_client_secret_here"
     ```
   - Click "Deploy"!

4. **Done!** Your app will be live in ~2 minutes at:
   ```
   https://your-app-name.streamlit.app
   ```

---

## Option 2: Run Locally (5 minutes)

**Perfect for development and testing**

### Prerequisites:
- Python 3.9+ installed
- Git installed

### Steps:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/consensuswatch.git
cd consensuswatch

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your Reddit API credentials

# 5. Run the web interface
streamlit run dashboard/app_new.py

# Or run the API
uvicorn api.main:app --reload
```

Your app will be available at:
- **Web Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## Option 3: Docker (One Command)

**Perfect for production-like environment**

### Prerequisites:
- Docker and Docker Compose installed

### Steps:

```bash
# 1. Clone and navigate
git clone https://github.com/yourusername/consensuswatch.git
cd consensuswatch

# 2. Create .env file with credentials
cp .env.example .env
# Edit .env file

# 3. Run everything with one command
docker-compose up --build

# Or use the deployment script
./deploy.sh
```

Access at:
- **Web Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **Redis**: localhost:6379

---

## Option 4: Deploy to Railway (Automated)

**Best for production deployment**

### Steps:

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set REDDIT_CLIENT_ID="your_id"
railway variables set REDDIT_CLIENT_SECRET="your_secret"

# 5. Deploy
railway up

# 6. Open your deployment
railway open
```

Your app will be live with a custom URL!

---

## First Time Setup

### Get Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Scroll to bottom and click "create another app..."
3. Fill in:
   - **name**: ConsensusWatch
   - **App type**: script
   - **description**: Bot detection tool
   - **about url**: (leave blank)
   - **redirect uri**: http://localhost:8501
4. Click "create app"
5. Copy the values:
   - **Client ID**: Under the app name (looks like: `dj38f9s...`)
   - **Client Secret**: Next to "secret"

---

## Using the App

### Analyze a Single Thread

1. Open the web dashboard
2. Navigate to "Analyze Thread"
3. Paste a Reddit URL like:
   ```
   https://www.reddit.com/r/worldnews/comments/abc123/...
   ```
4. Click "Analyze"
5. View comprehensive results with graphs!

### Batch Analysis

1. Go to "Batch Analysis"
2. Enter subreddit name (e.g., `worldnews`)
3. Set time window (e.g., 24 hours)
4. Click "Analyze Subreddit"
5. Review multiple threads at once!

### Using the API

```bash
# Example API request
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.reddit.com/r/..."}'
```

---

## Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "Reddit API Error"
- Check your credentials in `.env`
- Ensure your Reddit app is created correctly
- Verify you're not rate limited

### "Port already in use"
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run dashboard/app_new.py --server.port=8502
```

### Docker Issues
```bash
# Rebuild without cache
docker-compose build --no-cache

# View logs
docker-compose logs -f
```

---

## Next Steps

- **Read the docs**: Check out `docs/methodology.md`
- **Try batch analysis**: Analyze entire subreddits
- **Explore the API**: Visit http://localhost:8000/docs
- **Customize**: Modify thresholds in the code
- **Deploy**: Use `DEPLOYMENT.md` for production setup

---

## Getting Help

- **Documentation**: See `DEPLOYMENT.md` for detailed deployment guides
- **Issues**: Open an issue on GitHub
- **Questions**: Check existing issues or create new one

---

## Platform-Specific URLs

After deployment, your app will be available at:

- **Streamlit Cloud**: `https://[your-app-name].streamlit.app`
- **Railway**: `https://[your-app].railway.app`
- **Heroku**: `https://[your-app].herokuapp.com`
- **DigitalOcean**: `https://[your-app].ondigitalocean.app`
- **Local**: `http://localhost:8501`

---

## Architecture

```
┌─────────────────┐
│  Web Dashboard  │  (Streamlit)
│   Port: 8501    │
└────────┬────────┘
         │
    ┌────┴────┐
    │   API   │  (FastAPI)
    │Port:8000│
    └────┬────┘
         │
    ┌────┴────┐
    │  Redis  │  (Cache)
    │Port:6379│
    └─────────┘
```

---

**Ready to deploy? Choose an option above and you'll be live in minutes!** 🚀
