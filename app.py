from flask import Flask, redirect
from flask_talisman import Talisman
import random
import requests
from lib.arena import Arena

app = Flask(__name__)


# GET request to the channel
def get_channel(channel):
    """
    Returns the channel's HTML.
    """
    url = f'https://api.are.na/v2/channels/{channel}?per=1000'
    response = requests.get(url)
    data = response.json()
    contents = data['contents']
    # Usable content list only includes items with contents['source']['url']
    length = len(contents)
    return contents, length

@app.route('/')
def index():
    a = Arena()
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    return redirect(link)

Talisman(app, content_security_policy=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)