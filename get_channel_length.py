import math
import requests

def get_channel_pages(slug):
    per_page = 100  # Maximum items per page
    url = f"https://api.are.na/v2/channels/{slug}?per=0"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        length = data.get('length', 0)
        num_pages = math.ceil(length / per_page)
        return num_pages
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return None

if __name__ == "__main__":
    slug = input("Enter the are.na channel slug: ").strip()
    pages = get_channel_pages(slug)
    if pages is not None:
        print(f"The channel '{slug}' has {pages} pages.")
    else:
        print(f"Could not determine the number of pages for the channel '{slug}'.")