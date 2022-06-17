from lib.helpers import *
import requests


# # Search marginalia api with query
# def search(query):
# 	url = "https://api.marginalia.nu/{key}/search/{query}"
# 	response = requests.get(url.format(key='public', query=query))

# 	if response.ok:
# 		return response.json()
# 	else:
# 		return None

# def process_search(query):
# 	data = search(query)
# 	if data:
# 		results = data['results']
# 		random = random.choice(results)
# 		return random['url']
# 	else:
# 		return None

class Search:
	def __init__(self):
		self.base_url = 'https://api.marginalia.nu/public/search'
	
	def process_query(self, query):
		url = f'{self.base_url}/{query}'
		response = requests.get(url)
		if response.ok:
			return response.json()
		else:
			return None
	
	def get_link(self, query):
		data = self.process_query(query)
		if data:
			results = data['results']
			# random result 
			r = random.choice(results)
			return r['url']
		else:
			return None

#http://127.0.0.1:5000/search?query=never+lose