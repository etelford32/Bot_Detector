# Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Streamlit Community Cloud (Recommended - FREE)

**Easiest deployment for the web dashboard**

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file: `dashboard/app_new.py`
5. Add secrets in Streamlit dashboard:
   ```toml
   [secrets]
   REDDIT_CLIENT_ID = "your_client_id"
   REDDIT_CLIENT_SECRET = "your_client_secret"
   REDDIT_USER_AGENT = "ConsensusWatch/0.1.0"
   ```
6. Click "Deploy"!

**Pros**: Free, automatic SSL, easy updates
**Cons**: Limited resources, cold starts

---

### Option 2: Railway (Recommended - Paid)

**Best for production with API + Dashboard**

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login and initialize:
   ```bash
   railway login
   railway init
   ```

3. Add environment variables:
   ```bash
   railway variables set REDDIT_CLIENT_ID="your_id"
   railway variables set REDDIT_CLIENT_SECRET="your_secret"
   railway variables set REDDIT_USER_AGENT="ConsensusWatch/0.1.0"
   ```

4. Deploy:
   ```bash
   railway up
   ```

**Pros**: Easy, scales well, great DX
**Cons**: Paid (but generous free tier)

---

### Option 3: Docker + Any Cloud Platform

**Most flexible option**

#### Local Docker Testing:
```bash
# Build and run
docker-compose up --build

# Access:
# - Web dashboard: http://localhost:8501
# - API: http://localhost:8000
# - Redis: localhost:6379
```

#### Deploy to Various Platforms:

**Google Cloud Run:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/consensuswatch

# Deploy
gcloud run deploy consensuswatch \
  --image gcr.io/PROJECT_ID/consensuswatch \
  --platform managed \
  --port 8501 \
  --set-env-vars REDDIT_CLIENT_ID=xxx,REDDIT_CLIENT_SECRET=xxx
```

**AWS ECS/Fargate:**
```bash
# Build and push to ECR
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
docker build -t consensuswatch .
docker tag consensuswatch:latest aws_account_id.dkr.ecr.region.amazonaws.com/consensuswatch:latest
docker push aws_account_id.dkr.ecr.region.amazonaws.com/consensuswatch:latest

# Deploy using ECS console or CLI
```

**Azure Container Instances:**
```bash
# Create resource group
az group create --name consensuswatch-rg --location eastus

# Deploy
az container create \
  --resource-group consensuswatch-rg \
  --name consensuswatch \
  --image your-registry/consensuswatch \
  --dns-name-label consensuswatch \
  --ports 8501 \
  --environment-variables \
    REDDIT_CLIENT_ID=xxx \
    REDDIT_CLIENT_SECRET=xxx
```

**DigitalOcean App Platform:**
```bash
# Use doctl CLI
doctl apps create --spec .do/app.yaml
```

---

### Option 4: Heroku

**Traditional PaaS option**

1. Create `Procfile`:
   ```
   web: streamlit run dashboard/app_new.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create consensuswatch
   heroku config:set REDDIT_CLIENT_ID=xxx
   heroku config:set REDDIT_CLIENT_SECRET=xxx
   git push heroku main
   ```

---

### Option 5: Vercel (Serverless)

**For API deployment**

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Create `vercel.json`:
   ```json
   {
     "builds": [
       {"src": "api/main.py", "use": "@vercel/python"}
     ],
     "routes": [
       {"src": "/(.*)", "dest": "api/main.py"}
     ]
   }
   ```

3. Deploy:
   ```bash
   vercel --prod
   ```

---

## 🔧 Configuration

### Environment Variables

Required:
- `REDDIT_CLIENT_ID` - Your Reddit app client ID
- `REDDIT_CLIENT_SECRET` - Your Reddit app secret
- `REDDIT_USER_AGENT` - User agent string (default: ConsensusWatch/0.1.0)

Optional:
- `EMBEDDING_MODEL` - Sentence transformer model (default: all-MiniLM-L6-v2)
- `REDIS_HOST` - Redis host for caching (default: localhost)
- `REDIS_PORT` - Redis port (default: 6379)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)

### Getting Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - Name: ConsensusWatch
   - Type: Script
   - Redirect URI: http://localhost:8501
4. Copy the client ID and secret

---

## 📊 Monitoring & Scaling

### Health Checks

**Streamlit:**
```bash
curl http://your-app/_stcore/health
```

**API:**
```bash
curl http://your-app:8000/api/v1/health
```

### Performance Optimization

1. **Enable Redis Caching:**
   - Set `REDIS_HOST` environment variable
   - Reduces embedding computation time by 80%+

2. **Model Caching:**
   - First run downloads models (~100MB)
   - Use persistent volumes to cache models
   - Reduces cold start time

3. **Resource Requirements:**
   - **Minimum**: 512MB RAM, 1 vCPU
   - **Recommended**: 2GB RAM, 2 vCPU
   - **Optimal**: 4GB RAM, 4 vCPU (for batch analysis)

### Scaling Considerations

- **Vertical scaling**: Increase RAM for larger threads
- **Horizontal scaling**: Load balance multiple instances
- **Caching**: Use Redis for production
- **CDN**: Serve static assets via CDN
- **Database**: Consider PostgreSQL for results storage

---

## 🔒 Security Best Practices

1. **Never commit secrets:**
   - Use environment variables
   - Add `.env` to `.gitignore`
   - Use platform secret managers

2. **API Rate Limiting:**
   - Implement rate limiting on API endpoints
   - Respect Reddit API limits (60 req/min)

3. **Input Validation:**
   - Validate all user inputs
   - Sanitize URLs
   - Limit request sizes

4. **HTTPS Only:**
   - Enable SSL/TLS
   - Use platform-provided certificates
   - Redirect HTTP to HTTPS

---

## 🚨 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Rebuild with no cache
docker-compose build --no-cache
```

**Out of memory:**
```bash
# Increase Docker memory limit
# Or reduce batch size in app
```

**Redis connection failed:**
```bash
# Check Redis is running
docker-compose ps redis

# View Redis logs
docker-compose logs redis
```

**Model download fails:**
```bash
# Pre-download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Logs

**Docker Compose:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
```

**Streamlit Cloud:**
- Check logs in Streamlit dashboard
- Enable advanced logs in settings

**Railway:**
```bash
railway logs
```

---

## 📈 Post-Deployment

### Custom Domain

**Streamlit Cloud:**
1. Go to app settings
2. Add custom domain
3. Update DNS CNAME record

**Railway:**
```bash
railway domain
```

**Other platforms:**
- Follow platform-specific domain setup
- Update DNS records
- Enable SSL certificate

### Analytics

Add analytics to track usage:
- Google Analytics
- Plausible
- PostHog
- Custom event tracking

### Monitoring

Recommended tools:
- **Uptime**: UptimeRobot, Better Uptime
- **Performance**: New Relic, Datadog
- **Errors**: Sentry
- **Logs**: Papertrail, Logtail

---

## 🔄 CI/CD

See `.github/workflows/deploy.yml` for automated deployments.

### Automated Deploy on Push:

1. **Streamlit Cloud**: Automatic on git push
2. **Railway**: Set up GitHub integration
3. **Others**: Use GitHub Actions (included)

---

## 💰 Cost Estimates

**Free Tier Options:**
- Streamlit Community Cloud: FREE (with limits)
- Railway: $5/month free credit
- Heroku: $5-7/month (Eco dyno)
- Vercel: FREE (generous limits)

**Recommended Production:**
- Railway Hobby: ~$15-20/month
- Google Cloud Run: ~$10-30/month (pay per use)
- AWS Fargate: ~$20-40/month
- DigitalOcean: $12-24/month

---

## 📱 Progressive Web App (PWA)

The app is PWA-ready! Users can "install" it on mobile devices.

To enhance PWA features, add to `.streamlit/config.toml`:
```toml
[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[server]
enableCORS = false
enableXsrfProtection = true
```

---

## 🎯 Recommended Setup for Production

**Best Overall Setup:**
1. **Frontend (Dashboard)**: Streamlit Community Cloud (free)
2. **Backend (API)**: Railway with Redis (paid but cheap)
3. **Monitoring**: UptimeRobot (free) + Sentry (free tier)
4. **Domain**: Namecheap/Google Domains (~$12/year)
5. **Analytics**: Plausible or Google Analytics (free)

**Total Cost**: ~$5-15/month + domain

---

## 🆘 Support

- **Documentation**: See /docs folder
- **Issues**: GitHub Issues
- **Community**: GitHub Discussions
- **Email**: support@consensuswatch.io (if configured)
