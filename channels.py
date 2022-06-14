import random
from collections import Counter
import itertools
import numpy as np

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

def random_page(max):
	"""
	Returns a random page number given max pages.
	"""
	return random.randint(1, max)

# Channels dict with weights
channels = {
	f'internet-escape?page={random_page(11)}': 6,
	f'thirsty-for-knowledge?page={random_page(11)}': 5,
	f'bookmarks-1ntdk32bur0?page={random_page(6)}': 5,
	f'we-should-talk-about-this-website?page={random_page(6)}': 4,
	f'www-62v_kltr0d8?page={random_page(6)}': 4,
	f'site-cite-sight?page={random_page(3)}': 3,
	f'internet-surfing-clubs?page={random_page(2)}': 3,
	f'links-to-the-cultural-revolution' : 1,
}

weight_sum = sum(channels.values())

def weighted_random(d):
	"""
	Returns a random channel, weighted towards the beginning.
	"""
	r = random.randint(1, weight_sum)
	for k, v in d.items():
		r -= v
		if r <= 0:
			return k


print(weighted_random(channels))