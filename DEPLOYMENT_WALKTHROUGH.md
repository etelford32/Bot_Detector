# 🚀 Complete Deployment Walkthrough

## Step-by-Step Guide: From Zero to Live App

Follow this guide to deploy ConsensusWatch in ~15 minutes.

---

## Part 1: Create Reddit App & Get API Credentials

### Step 1: Create/Use Reddit Account

**Option A: Create New Account (Recommended for the app)**
1. Go to https://www.reddit.com/register
2. Fill in:
   - Email: `your-email@example.com`
   - Username: `ConsensusWatchBot` (or similar)
   - Password: (strong password)
3. Verify email
4. Log in

**Option B: Use Existing Account**
- Just log in to your current Reddit account

### Step 2: Create Reddit Application

1. **Go to Reddit Apps Page**
   - Visit: https://www.reddit.com/prefs/apps
   - Scroll to bottom
   - Click **"create another app..."** button

2. **Fill Out the Form**
   ```
   Name: ConsensusWatch

   App type: ○ web app
             ○ installed app
             ● script           [SELECT THIS ONE]

   Description: Bot detection and consensus analysis tool

   About url: https://github.com/yourusername/Bot_Detector

   Redirect uri: http://localhost:8501
   ```

3. **Click "create app"**

4. **Copy Your Credentials**

   You'll see something like this:
   ```
   ConsensusWatch                    [edit] [delete]
   personal use script

   ABCdef123GHI456                   ← This is your CLIENT_ID

   secret    jklMNO789pqrSTU012       ← This is your CLIENT_SECRET

   description: Bot detection...
   ```

5. **Save These Somewhere Safe**
   ```
   REDDIT_CLIENT_ID=ABCdef123GHI456
   REDDIT_CLIENT_SECRET=jklMNO789pqrSTU012
   REDDIT_USER_AGENT=ConsensusWatch/0.1.0
   ```

   ⚠️ **Keep these secret!** Don't share or commit to Git.

---

## Part 2: Deploy API Backend to Vercel

### Step 1: Install Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Or if you don't have npm, use:
# curl -sf https://vercel.com/install | sh
```

### Step 2: Login to Vercel

```bash
vercel login

# This will open browser for authentication
# Choose GitHub, GitLab, or Email
```

### Step 3: Configure Vercel for API

We need to update the Vercel config for proper deployment:

```bash
# Your vercel.json is already created!
# It's configured to deploy the API as serverless functions
```

### Step 4: Add Environment Variables to Vercel

**Option A: Via CLI (Recommended)**
```bash
# Navigate to project directory
cd /path/to/Bot_Detector

# Add secrets
vercel env add REDDIT_CLIENT_ID
# Paste your client ID when prompted

vercel env add REDDIT_CLIENT_SECRET
# Paste your client secret when prompted

vercel env add REDDIT_USER_AGENT
# Type: ConsensusWatch/0.1.0
```

**Option B: Via Web Dashboard** (After first deployment)
1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable

### Step 5: Deploy API to Vercel

```bash
# Initial deployment
vercel

# Answer the prompts:
# ? Set up and deploy? [Y/n] y
# ? Which scope? [Your account]
# ? Link to existing project? [N/y] n
# ? What's your project's name? consensuswatch-api
# ? In which directory is your code located? ./

# Wait for deployment...

# You'll get a URL like:
# https://consensuswatch-api-xxxxx.vercel.app
```

### Step 6: Deploy to Production

```bash
# Deploy to production
vercel --prod

# Your API is now live at:
# https://consensuswatch-api.vercel.app
```

### Step 7: Test Your API

```bash
# Test health endpoint
curl https://consensuswatch-api.vercel.app/api/v1/health

# Should return:
# {"status":"healthy","timestamp":"...","service":"consensuswatch-api","version":"0.1.0"}
```

---

## Part 3: Deploy Dashboard to Streamlit Cloud

### Step 1: Push Code to GitHub

```bash
# Make sure all changes are committed
git add -A
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Click **"Sign up"** or **"Sign in"**
   - Use GitHub account

2. **Create New App**
   - Click **"New app"** button
   - Or go to: https://share.streamlit.io/deploy

3. **Configure App**
   ```
   Repository: yourusername/Bot_Detector
   Branch: main (or your branch name)
   Main file path: dashboard/app_new.py
   ```

4. **Click "Advanced settings"**

5. **Add Secrets**

   In the "Secrets" text box, paste:
   ```toml
   # .streamlit/secrets.toml
   REDDIT_CLIENT_ID = "ABCdef123GHI456"
   REDDIT_CLIENT_SECRET = "jklMNO789pqrSTU012"
   REDDIT_USER_AGENT = "ConsensusWatch/0.1.0"
   ```

   ⚠️ Replace with YOUR actual credentials from Part 1!

6. **Click "Deploy!"**

7. **Wait 2-3 minutes** for deployment

8. **Your app will be live at:**
   ```
   https://yourusername-bot-detector-app-new-xxxxxx.streamlit.app
   ```

---

## Part 4: Connect Frontend to Backend (Optional)

If you want the Streamlit app to use your Vercel API:

### Update API Configuration

In your Streamlit app, you can configure the API URL:

```python
# In dashboard/app_new.py or a config file
API_BASE_URL = os.getenv("API_URL", "https://consensuswatch-api.vercel.app")
```

Add to Streamlit secrets:
```toml
API_URL = "https://consensuswatch-api.vercel.app"
```

---

## Part 5: Post-Deployment Steps

### ✅ Verify Everything Works

**1. Test the Dashboard**
- Visit your Streamlit URL
- Try the "Analyze Thread" page
- Paste a Reddit URL like:
  ```
  https://www.reddit.com/r/Python/comments/hot/
  ```
- Click "Analyze"
- Check results appear

**2. Test the API**
```bash
# Test analyze endpoint
curl -X POST "https://consensuswatch-api.vercel.app/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.reddit.com/r/Python/comments/..."}'
```

**3. Check Health Endpoints**
```bash
curl https://consensuswatch-api.vercel.app/api/v1/health
curl https://consensuswatch-api.vercel.app/api/v1/health/detailed
```

### 🎨 Customize Your Deployment

**Update App Name/URL (Streamlit)**
1. Go to https://share.streamlit.io
2. Click on your app
3. Settings → General → App URL
4. Change to custom name

**Add Custom Domain (Vercel)**
1. Go to Vercel dashboard
2. Your project → Settings → Domains
3. Add your domain
4. Follow DNS setup instructions

**Add Custom Domain (Streamlit)**
1. Streamlit Settings → General
2. Custom subdomain
3. Follow instructions

---

## Part 6: Enable Auto-Deploy on Git Push

### Streamlit (Already Enabled!)
- Every push to main branch auto-deploys
- No setup needed!

### Vercel
1. Go to project settings on Vercel
2. Git → Production Branch
3. Set to `main`
4. Every push to main auto-deploys!

---

## 🔧 Troubleshooting

### "Reddit API Error: Invalid Credentials"
- Double-check CLIENT_ID and CLIENT_SECRET
- Make sure no extra spaces
- Verify app type is "script" not "web app"

### "Module not found" on Vercel
- Check `requirements.txt` is in root
- Ensure all dependencies listed
- Try redeploying: `vercel --prod --force`

### "App won't load" on Streamlit
- Check logs in Streamlit dashboard
- Verify secrets are correct
- Check main file path is `dashboard/app_new.py`

### Vercel Serverless Timeout
- Vercel free tier has 10s timeout
- For long analyses, upgrade to Pro
- Or use Railway instead

---

## 📊 Your Live URLs

After deployment, you'll have:

✅ **Dashboard**: `https://[your-name]-bot-detector.streamlit.app`
✅ **API**: `https://consensuswatch-api.vercel.app`
✅ **API Docs**: `https://consensuswatch-api.vercel.app/docs`
✅ **Health**: `https://consensuswatch-api.vercel.app/api/v1/health`

---

## 🎯 Quick Command Reference

```bash
# Vercel Deployment
vercel login                    # Login
vercel env add VARIABLE_NAME    # Add env variable
vercel                          # Deploy to preview
vercel --prod                   # Deploy to production
vercel logs                     # View logs

# Check Status
vercel ls                       # List deployments
vercel inspect [url]            # Inspect deployment

# Streamlit
# Just push to GitHub - auto-deploys!
git push origin main
```

---

## 🔐 Security Checklist

✅ Never commit `.env` file
✅ Use Vercel environment variables
✅ Use Streamlit secrets
✅ Don't share CLIENT_SECRET publicly
✅ Enable 2FA on Reddit account
✅ Review Vercel security settings

---

## 💡 Pro Tips

1. **Monitor Usage**: Check Vercel dashboard for API usage
2. **Set Up Alerts**: Configure uptime monitoring (UptimeRobot)
3. **Custom Domain**: Makes it more professional
4. **Enable Analytics**: Track user engagement
5. **Rate Limiting**: Consider adding for production

---

## 🆘 Need Help?

- **Vercel Issues**: https://vercel.com/support
- **Streamlit Issues**: https://discuss.streamlit.io
- **Reddit API**: https://www.reddit.com/dev/api
- **Project Issues**: GitHub Issues

---

## 🎉 Next Steps

After deployment:

1. **Share your app!** Post on Reddit, Twitter, etc.
2. **Gather feedback** from users
3. **Monitor performance** and errors
4. **Iterate and improve** based on usage
5. **Consider upgrading** if you get high traffic

---

**Congratulations! Your app is now live! 🚀**

Share your URL and start detecting bots!
