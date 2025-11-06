# Vigent - Vercel Deployment Guide

## 🚀 Deploy to Vercel (FREE)

This guide will help you deploy your Vigent AI job application assistant to Vercel for free.

---

## 📁 Project Structure

```
vigent/
├── index.html                      # Static homepage (glassmorphism UI)
├── api/
│   ├── jobs.py                     # RSS feed fetching (Remotive + We Work Remotely)
│   └── generate-application.py     # AI cover letter & interview prep
├── vercel.json                     # Vercel configuration
├── requirements.txt                # Python dependencies
└── .env.example                    # Environment variables template
```

---

## 🔑 Prerequisites

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **Google Gemini API Key** - Get it from [ai.google.dev](https://ai.google.dev/)

---

## 📝 Step-by-Step Deployment

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click **"Get API Key"**
3. Create a new API key
4. Copy the key (starts with `AI...`)

### 2. Deploy to Vercel

#### Option A: Deploy from GitHub

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/vigent.git
   git push -u origin main
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Git Repository"
   - Select your `vigent` repository
   - Click "Deploy"

#### Option B: Deploy with Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Follow the prompts**:
   - Link to existing project? → No
   - Project name? → vigent (or your choice)
   - Directory? → ./
   - Deploy? → Yes

### 3. Add Environment Variable

1. Go to your project dashboard on Vercel
2. Click **Settings** → **Environment Variables**
3. Add:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key (from Step 1)
   - **Environment**: Production, Preview, Development (select all)
4. Click **Save**

### 4. Redeploy

- Go to **Deployments** tab
- Click **Redeploy** on the latest deployment
- Your app will be live in ~30 seconds! 🎉

---

## 🌐 Your Live URL

After deployment, Vercel gives you a free URL:
```
https://your-project-name.vercel.app
```

You can also add a **custom domain** for free in Vercel settings!

---

## ✨ Features

- ✅ **AI-Powered Cover Letters** - Gemini AI generates personalized cover letters
- ✅ **Interview Preparation** - 5 questions + AI-generated answers
- ✅ **Live Job Feeds** - Real-time jobs from Remotive & We Work Remotely
- ✅ **Resume Upload** - Store locally in browser (no backend needed)
- ✅ **Glassmorphism UI** - Modern dark blue/turquoise design
- ✅ **Mobile Responsive** - Works perfectly on all devices

---

## 🐛 Troubleshooting

### API Key Issues
- **Error**: "GEMINI_API_KEY not configured"
- **Fix**: Make sure you added the environment variable in Vercel settings and redeployed

### Serverless Function Timeout
- **Error**: "FUNCTION_INVOCATION_FAILED"
- **Cause**: RSS feeds taking too long or Gemini API slow
- **Fix**: Already handled with try-catch blocks. Verify your API key is valid.

### Jobs Not Loading
- **Check** the browser console (F12 → Console tab)
- **Common issue**: RSS feeds might be temporarily down
- **Solution**: Switch between "Upwork Jobs" and "Live Jobs" toggle

---

## 💰 Cost

- **Vercel Free Tier**: 100GB bandwidth/month
- **Gemini API**: Free tier includes generous requests
- **Total Monthly Cost**: $0 for hobby projects! 🎉

---

## 🔒 Security

- ✅ API keys stored as Vercel environment variables (never in code)
- ✅ CORS headers enabled for API endpoints
- ✅ Resume data stored in browser localStorage only
- ✅ No database = no data breaches

---

## 📚 Next Steps

1. **Custom Domain**: Add your domain in Vercel settings
2. **Analytics**: Add Vercel Analytics (free) to track users
3. **Monitoring**: Vercel automatically monitors uptime

---

## 🆘 Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Gemini API Docs**: [ai.google.dev/docs](https://ai.google.dev/docs)

---

**Enjoy your free AI-powered job application assistant! 🚀**
