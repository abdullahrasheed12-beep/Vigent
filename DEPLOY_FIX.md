# Vercel Deployment Fix - API Functions Not Working

## Problem
Both `/api/jobs` (live jobs) and `/api/generate-application` (cover letters) were returning errors on Vercel.

## Root Cause
The `requirements.txt` included Flask, gunicorn, and python-dotenv which are NOT compatible with Vercel's serverless Python runtime. These packages caused build conflicts and prevented the API functions from executing.

## Fix Applied
Simplified `requirements.txt` to only include packages needed for serverless functions:
- `google-generativeai` - For Gemini AI
- `feedparser` - For RSS job feeds

## Deploy Instructions

### 1. Push the fix to GitHub
```bash
git add requirements.txt
git commit -m "Fix: Remove Flask dependencies for Vercel serverless"
git push origin main
```

### 2. Vercel will auto-deploy
- Wait 1-2 minutes for automatic deployment
- OR manually redeploy: Vercel Dashboard → Deployments → Redeploy

### 3. Test your endpoints
After deployment, test these URLs:

**Test API health:**
```
https://your-app.vercel.app/api/test
```
Should show: `{"status": "ok", ...}`

**Test live jobs:**
```
https://your-app.vercel.app/api/jobs?source=all
```
Should show: `{"success": true, "jobs": [...]}`

**Test on the app:**
- Visit your app homepage
- Toggle to "Live Jobs" - Should load remote jobs
- Upload a resume and click "Apply Now" on any job - Should generate cover letter

## What Changed
- **Before**: requirements.txt had Flask (25+ dependencies for a web framework we don't need)
- **After**: requirements.txt has only 2 packages needed for the serverless APIs

This makes the Vercel build faster, smaller, and actually work! 🎉
