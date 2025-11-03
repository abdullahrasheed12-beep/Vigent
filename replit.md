# Vibe AI Agent - Project Documentation

## Project Overview
**Name**: Vibe AI Agent  
**Type**: AI-Powered Upwork Auto-Bidder Dashboard  
**Stack**: Flask (Python), HTML, Tailwind CSS, Google Gemini API  
**Status**: MVP Complete  
**Created**: November 3, 2025

## Purpose
A simple, professional web application that helps freelancers generate AI-powered proposals for Upwork jobs. The app displays mock job listings and uses Google Gemini to create personalized, professional proposals that users can edit and copy.

## Project Architecture

### Tech Stack
- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML templates (Jinja2), Tailwind CSS, Vanilla JavaScript
- **AI Integration**: Google Gemini API (via google-generativeai SDK)
- **Environment Management**: python-dotenv

### Directory Structure
```
/app.py                 # Flask application with routes and Gemini integration
/templates/
  └── index.html        # Main dashboard with job feed and proposal generator
/static/                # Static assets directory (currently unused, CSS via CDN)
/data/
  └── jobs.json        # Mock Upwork job listings (8 sample jobs)
/.env                   # Environment variables (not in repo)
/.env.example          # Template for environment configuration
/.gitignore           # Python gitignore
/README.md            # Comprehensive setup and usage documentation
/replit.md            # This file - project memory and preferences
```

### Key Features Implemented
1. **Job Feed Dashboard** - Displays 8 mock Upwork jobs with title, description, budget, skills, and posting time
2. **Real-time Search** - Client-side keyword filtering of job listings
3. **AI Proposal Generation** - Gemini-powered proposal creation based on job details
4. **Proposal Review Interface** - Editable textarea with generated proposals
5. **Copy to Clipboard** - One-click copying for manual posting to Upwork
6. **Regenerate Function** - Ability to generate new proposals for the same job
7. **Loading States** - Proper UX feedback during API calls
8. **Responsive Design** - Mobile-friendly Tailwind CSS layout

## Dependencies

### Python Packages (Installed)
- `flask` - Web framework
- `python-dotenv` - Environment variable management
- `google-generativeai` - Google Gemini API client

### Frontend (CDN)
- Tailwind CSS - Utility-first CSS framework

## Environment Configuration

### Required Environment Variables
- `GEMINI_API_KEY` - Google Gemini API key for AI proposal generation
- `SESSION_SECRET` - Flask session secret (auto-generated if not provided)

### Setup Steps
1. Copy `.env.example` to `.env`
2. Add Gemini API key from https://makersuite.google.com/app/apikey
3. Run Flask app on port 5000 (bound to 0.0.0.0 for Replit)

## API Routes

### `GET /`
- Renders main dashboard
- Loads jobs from `data/jobs.json`
- Returns `templates/index.html` with job data

### `POST /api/generate-proposal`
- Accepts JSON: `{title, description, budget}`
- Calls Gemini API with custom prompt
- Returns: `{success: true, proposal: "text"}` or error
- Uses `gemini-1.5-flash` model

## Recent Changes
**November 3, 2025** - Initial MVP Development
- Created complete Flask application structure
- Implemented 8 mock Upwork job listings
- Integrated Google Gemini API for proposal generation
- Built responsive dashboard with Tailwind CSS
- Added search/filter, copy-to-clipboard, and regenerate features
- Created comprehensive README with setup instructions and future roadmap
- Configured .gitignore for Python projects

## User Preferences
- **Simplicity First**: User requested simple, clean MVP without React - pure Flask + HTML templates
- **Professional UI**: Startup-style, minimal, modern design using Tailwind CSS
- **Clear Documentation**: README must explain setup, usage, and future enhancements
- **No Login/Database**: MVP focused on core functionality only
- **Structured for Growth**: Project organized for easy future Upwork API integration

## Development Notes

### AI Prompt Engineering
The Gemini prompt is designed to:
- Address client needs directly
- Highlight relevant experience
- Explain project approach
- Show enthusiasm and professionalism
- Include call-to-action
- Keep proposals concise (200-300 words)
- Avoid placeholder text

### Mock Data
`jobs.json` contains 8 diverse job listings covering:
- Python/AI development
- Full-stack (React/Node)
- Web scraping
- Mobile (Flutter)
- WordPress
- Computer Vision/ML
- DevOps (AWS)
- E-commerce (Shopify)

## Future Roadmap

### Phase 1: Real Data Integration
- Upwork RSS feed integration
- Live Upwork API connection (OAuth required)
- Advanced filtering and categories

### Phase 2: Personalization
- User profile settings
- Custom proposal templates
- AI tone/style preferences

### Phase 3: Automation
- Proposal history database
- Auto-submit via Upwork API
- Analytics dashboard

### Phase 4: Advanced Features
- Multi-user authentication
- A/B testing for proposals
- Job recommendation engine
- Browser extension

## Known Limitations
- Mock data only (no real Upwork integration yet)
- No user authentication or database
- Single-user prototype
- Manual copy-paste to Upwork required
- No proposal history tracking

## Deployment Considerations
- Bind to 0.0.0.0:5000 for Replit/cloud environments
- Ensure GEMINI_API_KEY is set in production environment
- Consider rate limiting for API calls
- Review Upwork ToS before implementing auto-submission
- Add caching to reduce API costs in production
