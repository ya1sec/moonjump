from flask import Flask, redirect, render_template, request, current_app, jsonify
from flask_talisman import Talisman
import random
import requests
from lib.arena import Arena, ArenaError
from lib.hn import Hack
from lib.search import Search
from lib.db import get_random_jumpable_site, mark_site_as_not_jumpable, init_db
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from requests.exceptions import ConnectionError, Timeout, RequestException

load_dotenv()

app = Flask(__name__, static_url_path='/static')

# Initialize the database
DB_PATH = "lib/sites.db"
init_db(DB_PATH)

# SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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


def check_embeddable(link):
    if not link or not link.startswith('https://'):
        return False, "Only https URLs can be embedded"

    try:
        response = requests.head(link, allow_redirects=True, timeout=5)
    except (ConnectionError, Timeout, RequestException) as e:
        return False, str(e)

    x_frame_options = response.headers.get('X-Frame-Options', '').upper()
    csp = response.headers.get('Content-Security-Policy', '')
    headers_allow_embedding = (
        x_frame_options not in ['DENY', 'SAMEORIGIN'] and
        'frame-ancestors' not in csp and
        'X-Frame-Options' not in csp
    )

    if not response.ok:
        return False, f"Status {response.status_code}"
    if not headers_allow_embedding:
        return False, "Blocked by X-Frame-Options or Content-Security-Policy"

    return True, None


def serialize_jump(candidate, source_kind=None, can_embed=True):
    source = candidate.get('source') or {}
    channel = candidate.get('channel') or {}
    link = candidate.get('url') or source.get('url')

    return {
        "url": link,
        "can_embed": can_embed,
        "metadata": {
            "source": source_kind or candidate.get('source_kind') or "local",
            "title": candidate.get('title') or source.get('title'),
            "block_id": candidate.get('id'),
            "block_type": candidate.get('type'),
            "channel_slug": channel.get('slug'),
            "channel_title": channel.get('title'),
            "curator": candidate.get('curator'),
            "curator_slug": candidate.get('curator_slug'),
            "connected_at": candidate.get('connected_at'),
            "connection_count": candidate.get('connection_count'),
        }
    }


def live_arena_jump_payload(mode="random", channel_slug=None, block_id=None, attempts=4):
    last_error = None

    for _ in range(attempts):
        try:
            candidate = Arena().get_jump(
                mode=mode,
                channel_slug=channel_slug,
                block_id=block_id,
            )
            link = candidate.get('url') or (candidate.get('source') or {}).get('url')
            can_embed, reason = check_embeddable(link)
            if can_embed:
                return serialize_jump(candidate, can_embed=True)
            last_error = reason
        except (ArenaError, RequestException, ValueError) as e:
            last_error = str(e)

    if last_error:
        print(f"Live Are.na jump failed: {last_error}")
    return None


def local_db_jump_payload(attempts=3):
    for _ in range(attempts):
        link = get_random_jumpable_site(DB_PATH)
        if not link:
            return None

        can_embed, reason = check_embeddable(link)
        if can_embed:
            return serialize_jump(
                {
                    "url": link,
                    "title": link,
                    "source_kind": "local:arena-cache",
                },
                can_embed=True,
            )

        print(f"Local site {link} is not jumpable: {reason}")
        mark_site_as_not_jumpable(link, DB_PATH)

    return None


def build_jump_payload():
    mode = request.args.get('mode', 'random')
    channel_slug = request.args.get('channel') or request.args.get('channel_slug')
    block_id = request.args.get('block_id')

    try:
        block_id = int(block_id) if block_id else None
    except ValueError:
        block_id = None

    if mode not in {"random", "same_channel", "drift"}:
        mode = "random"

    # Normal jumps remain random; these modes only constrain the random pool.
    payload = live_arena_jump_payload(
        mode=mode,
        channel_slug=channel_slug,
        block_id=block_id,
    )
    if payload:
        return payload

    payload = local_db_jump_payload()
    if payload:
        return payload

    try:
        link = Hack().serve()
        return serialize_jump(
            {"url": link, "title": link, "source_kind": "hacker-news"},
            can_embed=True,
        )
    except Exception as e:
        print(f"Hacker News fallback failed. {str(e)}")

    print("Falling back to Wikipedia")
    return serialize_jump(
        {
            "url": "https://en.wikipedia.org/wiki/Special:Random",
            "title": "Wikipedia Random",
            "source_kind": "wikipedia",
        },
        can_embed=True,
    )

# Serve index.html
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/jump')
def jump():
    return jsonify(build_jump_payload())


@app.route('/api/jump/next')
def api_jump_next():
    return jsonify(build_jump_payload())

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
