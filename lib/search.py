from lib.helpers import *
import requests
from bs4 import BeautifulSoup
import random
import re

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

	def random(self):
		url = 'https://search.marginalia.nu/explore/random'
		response = requests.get(url)
		if response.ok:
			soup = BeautifulSoup(response.text, 'html.parser')
			links = soup.select('section section a')
			if links:
				random_link = random.choice(links)
				href = random_link.get('href')

				if href:
					# Remove leading slashes and known prefixes
					href = re.sub(r'^/?(site/|explore/)?', '', href)

					# If href doesn't start with 'http://' or 'https://', try adding schemes
					if not href.startswith(('http://', 'https://')):
						# Try with 'https://' first
						https_url = f'https://{href}'
						try:
							resp = requests.head(https_url, timeout=5)
							if resp.ok:
								href = https_url
							else:
								# Try with 'http://' if 'https://' fails
								http_url = f'http://{href}'
								resp = requests.head(http_url, timeout=5)
								if resp.ok:
									href = http_url
								else:
									# Neither 'https://' nor 'http://' worked
									return None
						except requests.RequestException:
							# Exception occurred with 'https://', try 'http://'
							http_url = f'http://{href}'
							try:
								resp = requests.head(http_url, timeout=5)
								if resp.ok:
									href = http_url
								else:
									return None
							except requests.RequestException:
								# Neither scheme worked
								return None
					# If href already starts with 'http' or 'https', we assume it's valid
					return href
		return None

#http://127.0.0.1:5000/search?query=never+lose