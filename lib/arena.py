from lib.helpers import *
import requests

"""
NOTE: Channels
--------------

internet-escape
thirsty-for-knowledge
site-cite-sight
internet-surfing-clubs
we-should-talk-about-this-website
www-62v_kltr0d8
"""

##########
## MISC ##
##########

# Channels dict with weights
channels = {
	f'www-portfolios-and-studios?page={random_page(32)}': 8,
	f'internet-escape?page={random_page(11)}': 7,
	f'bookmarks-1ntdk32bur0?page={random_page(10)}': 6,
    f'dev-tools-y8yzn_83uci?page={random_page(17)}': 3,
	f'we-should-talk-about-this-website?page={random_page(7)}': 4,
	f'www-62v_kltr0d8?page={random_page(6)}': 4,
	f'site-cite-sight?page={random_page(3)}': 3,
    f'thirsty-for-knowledge?page={random_page(11)}': 3,
	f'internet-surfing-clubs?page={random_page(2)}': 3,
    # f'django-7kobd_9biyi?page={random_page(5)}': 1,
	# f'links-to-the-cultural-revolution' : 1,
}


def get_channel(channel):
    """
    Returns the channel's HTML.
    """
    url = f'https://api.are.na/v2/channels/{channel}&per=1000'
    response = requests.get(url)
    data = response.json()
    contents = data['contents'] # NOTE: Usable content list only includes items with contents['source']['url']
    length = len(contents)
    return contents, length


#############
## CLASSES ##
#############

# Are.na Class
class Arena:
    def __init__(self, channel=None):
        if channel == 'devtools':
            self.channel = f'dev-tools-y8yzn_83uci?page={random_page(17)}'
        elif channel == 'django':
            self.channel = f'django-7kobd_9biyi?page={random_page(5)}'
        elif channel == 'bookmarks':
            self.channel = f'bookmarks-1ntdk32bur0?page={random_page(6)}'
        else:
            self.channel = weighted_random(channels)
        
        print(f"Selected channel: {self.channel}")

    
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
