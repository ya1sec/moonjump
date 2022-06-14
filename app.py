from flask import Flask, redirect
import random
import requests
from channels import channels, weighted_random

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

class Arena:
    def __init__(self):
        self.channel = weighted_random(channels)
    
    def get_channel_contents(self):
        """
        Returns the channel's contents.
        """
        self.contents, self.length = get_channel(self.channel)
    
    def get_item_url(self):
        """
        Returns the item's URL.
        """
        self.item = random.choice(self.contents)
        try:
            link = self.item['source']['url']
        except Exception as e:
            self.item = random.choice(self.contents)
            link = self.item['source']['url']
            # link = None
        return link

@app.route('/')
def index():
    a = Arena()
    a.get_channel_contents()
    try:
        link = a.get_item_url()
    except Exception as e:
        link = a.get_item_url()
    return redirect(link)


if __name__ == '__main__':
    app.run(debug=True, port=5000)