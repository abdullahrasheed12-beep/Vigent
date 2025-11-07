from http.server import BaseHTTPRequestHandler
import json
import feedparser
from datetime import datetime
import logging

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query_params = {}
            if '?' in self.path:
                query_string = self.path.split('?')[1]
                for param in query_string.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        query_params[key] = value
            
            source = query_params.get('source', 'all')
            jobs = []
            
            # Remotive.io RSS feed
            if source in ['remotive', 'all']:
                try:
                    remotive_url = "https://remotive.com/api/remote-jobs/feed"
                    feed = feedparser.parse(remotive_url)
                    
                    for entry in feed.entries[:15]:
                        try:
                            pub_date_obj = None
                            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                pub_date_obj = datetime(*entry.published_parsed[:6])
                                pub_date_formatted = pub_date_obj.strftime('%B %d, %Y')
                            else:
                                pub_date_formatted = entry.get('published', 'N/A')
                            
                            summary = entry.get('summary', 'No description available')
                            if len(summary) > 250:
                                summary = summary[:250] + '...'
                            
                            title = entry.get('title', 'No Title')
                            job_type = 'Full-time'
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
                                'location': 'Remote',
                                'skills': []
                            }
                            jobs.append(job)
                        except Exception as e:
                            logging.error(f"Error parsing Remotive entry: {str(e)}")
                            continue
                except Exception as e:
                    logging.error(f"Error fetching Remotive feed: {str(e)}")
            
            # We Work Remotely RSS feed
            if source in ['wwremote', 'all']:
                try:
                    wwr_url = "https://weworkremotely.com/remote-jobs.rss"
                    feed = feedparser.parse(wwr_url)
                    
                    for entry in feed.entries[:15]:
                        try:
                            pub_date_obj = None
                            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                pub_date_obj = datetime(*entry.published_parsed[:6])
                                pub_date_formatted = pub_date_obj.strftime('%B %d, %Y')
                            else:
                                pub_date_formatted = entry.get('published', 'N/A')
                            
                            summary = entry.get('summary', 'No description available')
                            if len(summary) > 250:
                                summary = summary[:250] + '...'
                            
                            title = entry.get('title', 'No Title')
                            job_type = 'Full-time'
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
                                'location': 'Anywhere',
                                'skills': []
                            }
                            jobs.append(job)
                        except Exception as e:
                            logging.error(f"Error parsing WWR entry: {str(e)}")
                            continue
                except Exception as e:
                    logging.error(f"Error fetching WWR feed: {str(e)}")
            
            if not jobs:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'No jobs found from any source',
                    'jobs': []
                }).encode())
                return
            
            # Sort by publish date (newest first)
            jobs.sort(key=lambda x: x.get('published_date') or '', reverse=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'count': len(jobs),
                'source': source,
                'jobs': jobs
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': f'Failed to fetch jobs: {str(e)}',
                'jobs': []
            }).encode())
        
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
