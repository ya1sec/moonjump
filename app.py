from flask import Flask, redirect, render_template, request, current_app, jsonify
from flask_talisman import Talisman
import random
import requests
from lib.arena import Arena
from lib.hn import Hack
from lib.search import Search
from lib.db import get_random_jumpable_site
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__, static_url_path='/static')

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# class RandomWikipediaPage:
#     def __init__(self):
#         self.CATEGORIES = [
#             'philosophy_of_mind',
#             'computer_programming',
#             'pseudomathematics',
#         ]


#     def get_url(self):
#         base_url = 'https://en.wikipedia.org/wiki/Special:RandomInCategory/'
#         category = random.choice(self.CATEGORIES)
#         url = base_url + category
#         return url
class RandomWikipediaPage:
    def __init__(self):
        self.CATEGORIES = [
            'philosophy_of_mind',
            'computer_programming',
            'pseudomathematics',
            'carl_jung',
            'psychoanalysis',
        ]

    def get_url(self):
        # Nov 28 2024 override:
        return "https://en.wikipedia.org/wiki/Special:Random"
        # Pick a random category
        category = random.choice(self.CATEGORIES)

        # Use the Wikipedia API to get a list of pages in the chosen category
        url = f'https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:{category}&cmlimit=500&format=json'
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            pages = data.get('query', {}).get('categorymembers', [])

            # Choose a random page from the category
            if pages:
                random_page = random.choice(pages)
                page_title = random_page['title'].replace(' ', '_')
                return f'https://en.wikipedia.org/wiki/{page_title}'
        
        # Fallback in case of an error or no pages
        return f'https://en.wikipedia.org/wiki/Category:{category}'

# Serve index.html
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/jump')
def jump():
    link = get_random_jumpable_site(supabase_client)
    if link and link.startswith('https'):
        # Optional: Do a quick HEAD check to confirm it still allows framing:
        try:
            response = requests.head(link, allow_redirects=True, timeout=5)
            x_frame_options = response.headers.get('X-Frame-Options', '').upper()
            csp = response.headers.get('Content-Security-Policy', '')
            
            if (x_frame_options not in ['DENY', 'SAMEORIGIN'] and
                'frame-ancestors' not in csp and
                'X-Frame-Options' not in csp and
                response.ok):
                # Good enough—send it to the client
                return jsonify({"url": link, "can_embed": True})
        except Exception as e:
            print(f"Site {link} failed final check. {str(e)}")
    
    # If that fails or is None, fallback to Wikipedia:
    print("Falling back to Wikipedia")
    return jsonify({"url": "https://en.wikipedia.org/wiki/Special:Random", "can_embed": True})

@app.route('/old_jump')
def old_jump():
    max_attempts = 3  # Number of attempts before Wikipedia fallback
    
    for attempt in range(max_attempts):
        # Try Arena first
        try:
            a = Arena()
            a.get_channel_contents()
            link = a.get_item_url()
            if link and link.startswith('https'):
                print(f"Arena link (attempt {attempt + 1}): {link}")
                try:
                    # Check if the link is accessible and can be embedded
                    response = requests.head(link, allow_redirects=True, timeout=5)
                    
                    # Check for X-Frame-Options and Content-Security-Policy headers
                    x_frame_options = response.headers.get('X-Frame-Options', '').upper()
                    csp = response.headers.get('Content-Security-Policy', '')
                    
                    # Skip if site blocks framing
                    if (x_frame_options in ['DENY', 'SAMEORIGIN'] or 
                        'frame-ancestors' in csp or 
                        'X-Frame-Options' in csp):
                        print(f"Site blocks framing: {link}")
                        continue
                    
                    if response.status_code == 200:
                        # Try to actually connect to verify it works
                        test_response = requests.get(link, timeout=5)
                        if test_response.status_code == 200:
                            # Additional check for common blocking phrases in content
                            content = test_response.text.lower()
                            blocking_phrases = [
                                'blocked by chromium',
                                'security error',
                                'cannot be displayed in a frame',
                                'x-frame-options',
                                'refused to connect'
                            ]
                            if not any(phrase in content for phrase in blocking_phrases):
                                return jsonify({"url": link, "can_embed": True})
                            else:
                                print(f"Content contains blocking phrases: {link}")
                                continue
                except (requests.exceptions.ConnectionError, 
                       requests.exceptions.SSLError,
                       requests.exceptions.TooManyRedirects, 
                       requests.exceptions.RequestException,
                       requests.exceptions.Timeout) as e:
                    print(f"Connection error for Arena link: {str(e)}")
                    continue
        except Exception as e:
            print(f"Arena error (attempt {attempt + 1}): {str(e)}")

        # Try Marginalia
        try:
            link = Search().random()
            if link and link.startswith('https'):
                print(f"Marginalia link (attempt {attempt + 1}): {link}")
                try:
                    # Check if the link is accessible and can be embedded
                    response = requests.head(link, allow_redirects=True, timeout=5)
                    
                    # Check for X-Frame-Options and Content-Security-Policy headers
                    x_frame_options = response.headers.get('X-Frame-Options', '').upper()
                    csp = response.headers.get('Content-Security-Policy', '')
                    
                    # Skip if site blocks framing
                    if (x_frame_options in ['DENY', 'SAMEORIGIN'] or 
                        'frame-ancestors' in csp or 
                        'X-Frame-Options' in csp):
                        print(f"Site blocks framing: {link}")
                        continue
                    
                    if response.status_code == 200:
                        # Try to actually connect to verify it works
                        test_response = requests.get(link, timeout=5)
                        if test_response.status_code == 200:
                            # Additional check for common blocking phrases in content
                            content = test_response.text.lower()
                            blocking_phrases = [
                                'blocked by chromium',
                                'security error',
                                'cannot be displayed in a frame',
                                'x-frame-options',
                                'refused to connect'
                            ]
                            if not any(phrase in content for phrase in blocking_phrases):
                                return jsonify({"url": link, "can_embed": True})
                            else:
                                print(f"Content contains blocking phrases: {link}")
                                continue
                except (requests.exceptions.ConnectionError,
                       requests.exceptions.SSLError,
                       requests.exceptions.TooManyRedirects,
                       requests.exceptions.RequestException,
                       requests.exceptions.Timeout) as e:
                    print(f"Connection error for Marginalia link: {str(e)}")
                    continue
        except Exception as e:
            print(f"Marginalia error (attempt {attempt + 1}): {str(e)}")
        
        print(f"Both sources failed on attempt {attempt + 1}, trying again...")

    # Fall back to Wikipedia only after all attempts fail
    print("All attempts failed, falling back to Wikipedia")
    return jsonify({"url": "https://en.wikipedia.org/wiki/Special:Random", "can_embed": True})

@app.route('/fetch-content', methods=['POST'])
def fetch_content():
    url = request.json['url']
    try:
        response = requests.get(url)
        return jsonify({
            'content': response.text,
            'content_type': response.headers.get('Content-Type', '')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# random
@app.route('/marginalia_random')
def marginalia_random():
    try:
        link = Search().random()
        return redirect(link)
    except Exception as e:
        return redirect('/hn')

@app.route('/arena')
def arena():
    a = Arena()
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    try:
        return redirect(link)
    except Exception as e:
        return redirect('https://moonjump.app/arena')

@app.route('/devtools')
def devtools():
    a = Arena(channel='devtools')
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    try:
        return redirect(link)
    except Exception as e:
        return redirect('https://moonjump.app/devtools')

@app.route('/django')
def django():
    a = Arena(channel='django')
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    try:
        return redirect(link)
    except Exception as e:
        return redirect('https://moonjump.app/django')

@app.route('/bookmarks')
def bookmarks():
    a = Arena(channel='bookmarks')
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    try:
        return redirect(link)
    except Exception as e:
        return redirect('https://moonjump.app/bookmarks')

@app.route('/hn')
def hn():
    h = Hack()
    link = h.serve()
    try:
        return redirect(link)
    except Exception as e:
        return redirect('https://moonjump.app/hn')

@app.route('/search')
def search():
    # Get query parameter, default to empty string if not provided
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "No search query provided"}), 400
        
    # Replace spaces with +
    query = query.replace(' ', '+')
    s = Search()
    link = s.get_link(query)
    try:
        return jsonify({"url": link, "can_embed": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Talisman(app, content_security_policy=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)