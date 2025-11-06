import os
import json
import feedparser
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route('/')
def index():
    with open('data/jobs.json', 'r') as f:
        jobs = json.load(f)
    return render_template('index.html', jobs=jobs)

@app.route('/api/generate-proposal', methods=['POST'])
def generate_proposal():
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                'error': 'GEMINI_API_KEY not configured. Please add your API key to the .env file.'
            }), 400
        
        data = request.json
        job_title = data.get('title', '')
        job_description = data.get('description', '')
        job_budget = data.get('budget', '')
        
        prompt = f"""You are an expert freelance proposal writer. Write a compelling, professional Upwork proposal for the following job.

Job Title: {job_title}

Job Description: {job_description}

Budget: {job_budget}

Write a personalized proposal that:
1. Directly addresses the client's needs
2. Highlights relevant experience and skills
3. Explains your approach to the project
4. Shows enthusiasm and professionalism
5. Includes a brief call-to-action
6. Is concise (200-300 words)

Do not include placeholder text like [Your Name] or generic statements. Write as if you are a skilled freelancer with relevant experience."""

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        if not response or not hasattr(response, 'text') or not response.text:
            return jsonify({
                'error': 'Gemini API returned empty response. This may be due to safety filters or content blocks.'
            }), 400
        
        proposal_text = response.text
        
        return jsonify({
            'proposal': proposal_text,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error generating proposal: {str(e)}'
        }), 500

@app.route('/api/jobs')
def get_remote_jobs():
    """
    Fetch live job listings from remote job board RSS feeds.
    Query parameters:
    - source: Job board source (remotive, wwremote, or all)
    """
    try:
        source = request.args.get('source', 'all')
        
        jobs = []
        
        # Remotive.io RSS feed
        if source in ['remotive', 'all']:
            try:
                app.logger.info("Fetching Remotive.io RSS feed")
                remotive_url = "https://remotive.com/api/remote-jobs/feed"
                feed = feedparser.parse(remotive_url)
                
                for entry in feed.entries[:15]:
                    try:
                        pub_date = entry.get('published', 'N/A')
                        pub_date_obj = None
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            pub_date_obj = datetime(*entry.published_parsed[:6])
                            pub_date_formatted = pub_date_obj.strftime('%B %d, %Y')
                        else:
                            pub_date_formatted = pub_date
                        
                        summary = entry.get('summary', 'No description available')
                        if len(summary) > 250:
                            summary = summary[:250] + '...'
                        
                        # Extract job type and location from title or description
                        title = entry.get('title', 'No Title')
                        job_type = 'Full-time'
                        location = 'Remote'
                        
                        if 'part-time' in title.lower() or 'part time' in summary.lower():
                            job_type = 'Part-time'
                        if 'contract' in title.lower() or 'freelance' in title.lower():
                            job_type = 'Contract'
                        
                        job = {
                            'id': hash(entry.get('link', '')),
                            'title': title,
                            'link': entry.get('link', '#'),
                            'description': summary,
                            'summary': summary,
                            'published': pub_date_formatted,
                            'published_date': pub_date_obj.isoformat() if pub_date_obj else None,
                            'posted': pub_date_formatted,
                            'source': 'Remotive',
                            'budget': 'See job posting',
                            'job_type': job_type,
                            'location': location,
                            'skills': []
                        }
                        jobs.append(job)
                    except Exception as e:
                        app.logger.error(f"Error parsing Remotive entry: {str(e)}")
                        continue
            except Exception as e:
                app.logger.error(f"Error fetching Remotive feed: {str(e)}")
        
        # We Work Remotely RSS feed
        if source in ['wwremote', 'all']:
            try:
                app.logger.info("Fetching We Work Remotely RSS feed")
                wwr_url = "https://weworkremotely.com/remote-jobs.rss"
                feed = feedparser.parse(wwr_url)
                
                for entry in feed.entries[:15]:
                    try:
                        pub_date = entry.get('published', 'N/A')
                        pub_date_obj = None
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            pub_date_obj = datetime(*entry.published_parsed[:6])
                            pub_date_formatted = pub_date_obj.strftime('%B %d, %Y')
                        else:
                            pub_date_formatted = pub_date
                        
                        summary = entry.get('summary', 'No description available')
                        if len(summary) > 250:
                            summary = summary[:250] + '...'
                        
                        title = entry.get('title', 'No Title')
                        job_type = 'Full-time'
                        location = 'Anywhere'
                        
                        if 'part-time' in title.lower() or 'part time' in summary.lower():
                            job_type = 'Part-time'
                        if 'contract' in title.lower() or 'freelance' in title.lower():
                            job_type = 'Contract'
                        
                        job = {
                            'id': hash(entry.get('link', '') + 'wwr'),
                            'title': title,
                            'link': entry.get('link', '#'),
                            'description': summary,
                            'summary': summary,
                            'published': pub_date_formatted,
                            'published_date': pub_date_obj.isoformat() if pub_date_obj else None,
                            'posted': pub_date_formatted,
                            'source': 'We Work Remotely',
                            'budget': 'See job posting',
                            'job_type': job_type,
                            'location': location,
                            'skills': []
                        }
                        jobs.append(job)
                    except Exception as e:
                        app.logger.error(f"Error parsing WWR entry: {str(e)}")
                        continue
            except Exception as e:
                app.logger.error(f"Error fetching WWR feed: {str(e)}")
        
        if not jobs:
            return jsonify({
                'success': False,
                'error': 'No jobs found from any source',
                'jobs': []
            }), 404
        
        # Sort by publish date (newest first)
        jobs.sort(key=lambda x: x.get('published_date') or '', reverse=True)
        
        return jsonify({
            'success': True,
            'count': len(jobs),
            'source': source,
            'jobs': jobs
        })
    
    except Exception as e:
        app.logger.error(f"Error fetching remote jobs: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to fetch jobs: {str(e)}',
            'jobs': []
        }), 500

@app.route('/callback')
def oauth_callback():
    """
    OAuth callback route for Upwork integration.
    This endpoint handles the OAuth redirect from Upwork after user authorization.
    
    Expected query parameters:
    - code: Authorization code from Upwork
    - state: State parameter for CSRF protection
    
    Callback URL to configure in Upwork API settings:
    https://bid-genius-dashboard.vercel.app/callback
    """
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        
        print("=" * 60)
        print("UPWORK OAUTH CALLBACK RECEIVED")
        print("=" * 60)
        print(f"Authorization Code: {code}")
        print(f"State Parameter: {state}")
        print(f"Full Query String: {request.query_string.decode('utf-8')}")
        print("=" * 60)
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Missing authorization code'
            }), 400
        
        app.logger.info(f"OAuth callback received - Code: {code[:10]}..., State: {state}")
        
        return redirect(url_for('index'))
        
    except Exception as e:
        app.logger.error(f"Error in OAuth callback: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'OAuth callback error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
