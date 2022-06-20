from flask import Flask, redirect, render_template, request, current_app
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
    types = ['arena', 'hack']
    random_type = random.choice(types)
    if random_type == 'arena':
        return redirect('/arena')
    elif random_type == 'hack':
        return redirect('/hack')


@app.route('/arena')
def arena():
    a = Arena()
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    return redirect(link)

@app.route('/hn')
def hn():
    h = Hack()
    link = h.serve()
    return redirect(link)

@app.route('/search')
def search():
    # Accept query from user, replace spaces with +
    query = request.args.get('query')
    query = query.replace(' ', '+')
    s = Search()
    link = s.get_link(query)
    return redirect(link)

# Talisman(app, content_security_policy=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)