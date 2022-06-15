from lib.helpers import *
import requests

def get_data(url):
    """
    Returns the channel's HTML.
    """
    response = requests.get(url)
    data = response.json()
    return data


class Hack:
	def __init__(self):
		self.base_url = 'https://hacker-news.firebaseio.com/v0'
	
	def random_category(self):
		"""
		Returns a random category.
		"""
		categories = ['topstories', 'beststories', 'newstories']
		return random.choice(categories)
	
	def random_id(self, category):
		"""
		Returns a random id from the given category.
		- topstories
		- beststories
		- newstories
		"""
		url = f'{self.base_url}/{category}.json?print=pretty'
		data = get_data(url)
		story_id = random.choice(data)
		return story_id
	
	def get_item(self, id):
		"""
		Returns the item's data.
		"""
		url = f'{self.base_url}/item/{id}.json?print=pretty'
		data = get_data(url)
		link = data['url']
		return link
	
	def serve(self):
		"""
		Returns a random item's URL.
		"""
		category = self.random_category()
		print(category)
		id = self.random_id(category)
		print(id)
		link = self.get_item(id)
		print(link)
		return link
