from flask import Flask, redirect, render_template, request, current_app, jsonify
from flask_talisman import Talisman
import random
import requests
from lib.arena import Arena
from lib.hn import Hack
from lib.search import Search

app = Flask(__name__, static_url_path='/static')

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
    types = ['arena', 'arena', 'marginalia', 'marginalia', 'wikipedia']
    max_attempts = 5  # Maximum number of attempts to find a working link

    for _ in range(max_attempts):
        random_type = random.choice(types)
        try:
            if random_type == 'arena':
                a = Arena()
                a.get_channel_contents()
                link = a.get_item_url()
                if not link.startswith('https'):
                    print("No https, getting another link")
                    continue
                print(f"Arena link: {link}")
            elif random_type == 'wikipedia':
                link = RandomWikipediaPage().get_url()
            else:
                link = Search().random()
                if not link:
                    print("No link found from marginalia, getting WIKI link")
                    link = RandomWikipediaPage().get_url()
                    # continue
                if not link.startswith('https'):
                    print("No https, getting another link")
                    # print("No https, getting WIKI link")
                    # link = RandomWikipediaPage().get_url()
                    continue
                print(f"Random link: {link}")

            # Check if the link is accessible and can be embedded
            response = requests.head(link, allow_redirects=True, timeout=5)
            if response.headers.get('X-Frame-Options') in ['DENY', 'SAMEORIGIN']:
                print("X-Frame-Options is set to DENY or SAMEORIGIN, getting another link")
                continue
            if response.status_code == 200:
                return jsonify({"url": link, "can_embed": True})
            else:
                print(f"Link {link} is not accessible.")

        except Exception as e:
            print(f"Error: {str(e)}")

    # If no working link is found after max_attempts, return a fallback URL
    return jsonify({"url": RandomWikipediaPage().get_url(), "can_embed": True})

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
    # Accept query from user, replace spaces with +
    query = request.args.get('query')
    query = query.replace(' ', '+')
    s = Search()
    link = s.get_link(query)
    try:
        return redirect(link)
    except Exception as e:
        return redirect('https://moonjump.app')

# Talisman(app, content_security_policy=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)