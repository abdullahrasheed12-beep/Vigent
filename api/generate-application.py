from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai

# Configure Gemini AI
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if not GEMINI_API_KEY:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'GEMINI_API_KEY not configured'
                }).encode())
                return
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            job = data.get('job', {})
            resume = data.get('resume', '')
            
            if not resume:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Resume text is required'
                }).encode())
                return
            
            job_title = job.get('title', '')
            job_description = job.get('description', '')
            
            # Generate cover letter
            cover_letter_prompt = f"""You are an expert career coach. Write a compelling, professional cover letter for this job application.

Job Title: {job_title}

Job Description: {job_description}

Candidate's Resume:
{resume}

Write a personalized cover letter that:
1. Directly addresses the job requirements
2. Highlights relevant experience from the resume
3. Shows genuine interest in the role
4. Is professional yet personable
5. Is concise (250-350 words)

Write the cover letter in first person, ready to copy and paste. Do not include placeholders like [Date] or [Company Name]."""

            # Generate interview questions
            questions_prompt = f"""You are an expert interviewer. Based on this job description, generate 5 common interview questions that would likely be asked.

Job Title: {job_title}

Job Description: {job_description}

Generate 5 realistic interview questions that:
1. Focus on key skills and requirements from the job description
2. Are commonly asked in real interviews
3. Are specific to this role
4. Range from technical to behavioral

Return ONLY a JSON array of questions, like this:
["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]"""

            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Generate cover letter
            cover_response = model.generate_content(cover_letter_prompt)
            if not cover_response or not hasattr(cover_response, 'text') or not cover_response.text:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Failed to generate cover letter'
                }).encode())
                return
            
            cover_letter = cover_response.text
            
            # Generate questions
            questions_response = model.generate_content(questions_prompt)
            if not questions_response or not hasattr(questions_response, 'text') or not questions_response.text:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Failed to generate interview questions'
                }).encode())
                return
            
            # Parse questions
            try:
                questions_text = questions_response.text.strip()
                
                # Remove markdown code fences if present
                if questions_text.startswith('```'):
                    first_newline = questions_text.find('\n')
                    if first_newline != -1:
                        questions_text = questions_text[first_newline + 1:]
                    if questions_text.endswith('```'):
                        questions_text = questions_text[:-3]
                    questions_text = questions_text.strip()
                
                # Try to parse as JSON array
                if questions_text.startswith('[') and questions_text.endswith(']'):
                    parsed_questions = json.loads(questions_text)
                    questions_list = [
                        q.strip() for q in parsed_questions 
                        if isinstance(q, str) and len(q.strip()) > 10
                    ]
                else:
                    # Fallback: parse line-by-line
                    lines = [line.strip('- 0123456789."\'') for line in questions_text.split('\n')]
                    questions_list = [
                        q for q in lines 
                        if q and len(q) > 10 and not q.lower().startswith('json')
                    ]
                
                if not questions_list or len(questions_list) < 3:
                    raise ValueError("Insufficient valid questions parsed")
                    
            except Exception as e:
                # Fallback questions
                questions_list = [
                    "Tell me about your relevant experience for this role.",
                    "What interests you about this position?",
                    "Describe a challenging project you've worked on.",
                    "What are your salary expectations?",
                    "Where do you see yourself in 3 years?"
                ]
            
            # Generate answers for each question
            qa_pairs = []
            for question in questions_list[:5]:
                answer_prompt = f"""You are helping a job candidate prepare for an interview. Based on their resume, generate a strong, concise answer to this interview question.

Interview Question: {question}

Candidate's Resume:
{resume}

Generate a professional, concise answer (2-3 sentences) that:
1. Directly answers the question
2. References specific experience from the resume when relevant
3. Is confident and professional
4. Uses first person ("I have...")

Return ONLY the answer text, no introduction or explanation."""

                answer_response = model.generate_content(answer_prompt)
                if answer_response and hasattr(answer_response, 'text') and answer_response.text:
                    answer = answer_response.text.strip()
                else:
                    answer = "Based on my experience outlined in my resume, I have the relevant skills and background for this aspect of the role."
                
                qa_pairs.append({
                    'question': question,
                    'answer': answer
                })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'cover_letter': cover_letter,
                'questions': qa_pairs
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': f'Error generating application: {str(e)}'
            }).encode())
        
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
