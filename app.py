import os
import json
from flask import Flask, render_template, request, jsonify
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

        model = genai.GenerativeModel('gemini-1.5-flash')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
