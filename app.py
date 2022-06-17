from flask import Flask, redirect, request
from flask_talisman import Talisman
import random
import requests
from lib.arena import Arena
from lib.hn import Hack
from lib.search import Search

app = Flask(__name__)

@app.route('/')
def index():
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