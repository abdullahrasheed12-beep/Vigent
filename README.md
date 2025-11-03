# Vibe AI Agent - AI-Powered Upwork Auto-Bidder

A simple, professional MVP web application that helps freelancers generate AI-powered proposals for Upwork jobs using Google Gemini.

## Features

✅ **Job Feed Dashboard** - Browse mock Upwork job listings with detailed information  
✅ **Smart Search** - Filter jobs by keyword in real-time  
✅ **AI Proposal Generator** - Generate personalized proposals using Google Gemini API  
✅ **Proposal Editor** - Edit and customize AI-generated proposals  
✅ **Copy to Clipboard** - One-click copying for easy posting to Upwork  
✅ **Clean UI** - Modern, responsive design built with Tailwind CSS  

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **AI**: Google Gemini API
- **Environment**: python-dotenv for configuration

## Project Structure

```
vibe-ai-agent/
├── app.py                 # Flask backend with API routes
├── templates/
│   └── index.html        # Main dashboard interface
├── static/               # Static assets (CSS, JS if needed)
├── data/
│   └── jobs.json        # Mock Upwork job listings
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Template for environment variables
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.11+ installed
- A Google Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### 2. Install Dependencies

Dependencies are already installed in the Replit environment:
- Flask
- python-dotenv
- google-generativeai

If running locally, install via:
```bash
pip install flask python-dotenv google-generativeai
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Add your Google Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SESSION_SECRET=your_random_secret_key_here
```

### 4. Run the Application

```bash
python app.py
```

The app will be available at `http://0.0.0.0:5000`

## How to Use

1. **Browse Jobs** - View the list of mock Upwork jobs in the dashboard
2. **Search Jobs** - Use the search bar to filter jobs by keyword
3. **Generate Proposal** - Click "Generate Proposal" on any job
4. **Review & Edit** - The AI will generate a personalized proposal that you can edit
5. **Copy & Use** - Click "Copy to Clipboard" and paste into Upwork
6. **Regenerate** - Not happy with the proposal? Click "Regenerate" for a new version

## Customizing Job Listings

Edit `data/jobs.json` to add, remove, or modify job listings:

```json
{
  "id": 1,
  "title": "Job Title Here",
  "description": "Detailed job description...",
  "budget": "$1,000 - $2,000",
  "posted": "2 hours ago",
  "skills": ["Python", "Flask", "AI"],
  "duration": "2-3 weeks"
}
```

## Future Enhancements

### Phase 1: Real Data Integration
- [ ] Integrate Upwork RSS feed for real-time job listings
- [ ] Connect to Upwork API for live data (requires OAuth)
- [ ] Add job category filters and advanced search

### Phase 2: User Personalization
- [ ] User profile settings (skills, experience, portfolio links)
- [ ] Custom proposal templates
- [ ] Tone and style preferences for AI generation

### Phase 3: Automation & Tracking
- [ ] Proposal history database
- [ ] Auto-submit proposals via Upwork API
- [ ] Analytics dashboard (response rates, success metrics)
- [ ] Multiple AI model support (GPT-4, Claude, etc.)

### Phase 4: Advanced Features
- [ ] User authentication and multi-user support
- [ ] Proposal A/B testing
- [ ] Budget and job recommendation engine
- [ ] Browser extension for one-click proposal generation

## API Endpoints

### `GET /`
Returns the main dashboard with job listings

### `POST /api/generate-proposal`
Generates an AI proposal for a job

**Request Body:**
```json
{
  "title": "Job Title",
  "description": "Job Description",
  "budget": "$1,000 - $2,000"
}
```

**Response:**
```json
{
  "success": true,
  "proposal": "Generated proposal text..."
}
```

## Troubleshooting

### API Key Issues
- Make sure your `.env` file contains a valid `GEMINI_API_KEY`
- Verify the API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Check that you have API quota available

### Jobs Not Displaying
- Verify `data/jobs.json` exists and contains valid JSON
- Check browser console for JavaScript errors

### Proposal Generation Fails
- Check the Flask console for error messages
- Ensure you have internet connectivity for API calls
- Verify your Gemini API key is active and has quota

## Contributing

This is an MVP prototype. Contributions and suggestions are welcome!

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contact

For questions or feedback about this prototype, please create an issue or reach out.

---

**Note**: This is a prototype application. Before using in production:
- Add proper error handling and validation
- Implement rate limiting for API calls
- Add user authentication if handling sensitive data
- Review and comply with Upwork's Terms of Service
- Consider implementing caching to reduce API costs
