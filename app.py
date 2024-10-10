from flask import Flask, redirect, render_template, request, current_app, jsonify
from flask_talisman import Talisman
import random
import requests
from lib.arena import Arena
from lib.hn import Hack
from lib.search import Search

app = Flask(__name__, static_url_path='/static')

# Serve index.html
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/jump')
def jump():
    types = ['arena', 'marginalia']
    max_attempts = 5  # Maximum number of attempts to find a working link

    for _ in range(max_attempts):
        random_type = random.choice(types)
        try:
            if random_type == 'arena':
                a = Arena()
                a.get_channel_contents()
                link = a.get_item_url()
            else:
                link = Search().random()
                print(f"Random link: {link}")
                return link

            # Check if the link is accessible
            response = requests.head(link, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return link
            else:
                print(f"Link {link} is not accessible.")
        except Exception as e:
            return redirect('/jump')
    
    # If no working link is found after max_attempts, return a fallback URL
    return 'https://moonjump.app/jump'

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