from lib.helpers import weighted_random
import requests
import random

# Default headers for Are.na API requests
HEADERS = {
    'User-Agent': 'Moonjump/1.0',
    'Accept': 'application/json',
}

# Channel slugs with weights (no hardcoded page counts)
CHANNELS = {
    'www-portfolios-and-studios': 8,
    'internet-escape': 7,
    'bookmarks-1ntdk32bur0': 6,
    'dev-tools-y8yzn_83uci': 3,
    'we-should-talk-about-this-website': 4,
    'www-62v_kltr0d8': 4,
    'site-cite-sight': 3,
    'thirsty-for-knowledge': 3,
    'internet-surfing-clubs': 3,
}

# Named channel aliases for specific routes
CHANNEL_ALIASES = {
    'devtools': 'dev-tools-y8yzn_83uci',
    'django': 'django-7kobd_9biyi',
    'bookmarks': 'bookmarks-1ntdk32bur0',
}

# Items per page for pagination (smaller = faster responses)
ITEMS_PER_PAGE = 25


def get_channel_metadata(slug, per=ITEMS_PER_PAGE):
    """
    Fetch channel metadata to get total_pages dynamically.
    Uses per=1 to minimize payload size, then calculates pages for desired per value.
    """
    url = f'https://api.are.na/v2/channels/{slug}?per=1'
    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.ok:
        data = response.json()
        length = data.get('length', 0)
        # Calculate total_pages for our desired per value
        total_pages = max(1, (length + per - 1) // per)
        return {
            'total_pages': total_pages,
            'length': length,
        }
    return None


def get_channel_contents(slug, page=1, per=ITEMS_PER_PAGE):
    """
    Fetch channel contents for a specific page using the /contents endpoint.
    More efficient than fetching full channel representation.
    """
    url = f'https://api.are.na/v2/channels/{slug}/contents?page={page}&per={per}'
    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.ok:
        data = response.json()
        # Contents endpoint returns {'contents': [...]}
        return data.get('contents', [])
    return []


class Arena:
    def __init__(self, channel=None):
        # Resolve channel alias or use weighted random selection
        if channel and channel in CHANNEL_ALIASES:
            self.slug = CHANNEL_ALIASES[channel]
        elif channel:
            self.slug = channel
        else:
            self.slug = weighted_random(CHANNELS)

        self.contents = []
        print(f"Selected channel: {self.slug}")

    def get_channel_contents(self):
        """
        Fetch contents using dynamic pagination.
        1. Get metadata to find total_pages
        2. Pick a random page
        3. Fetch just that page's contents
        """
        # Get metadata for total_pages
        metadata = get_channel_metadata(self.slug)
        if not metadata:
            print(f"Failed to fetch metadata for {self.slug}")
            return

        total_pages = metadata['total_pages']

        # Pick a random page
        page = random.randint(1, max(1, total_pages))
        print(f"Fetching page {page}/{total_pages} from {self.slug}")

        # Fetch that page's contents
        self.contents = get_channel_contents(self.slug, page=page, per=ITEMS_PER_PAGE)

    def get_item_url(self):
        """
        Returns URL from a block, prioritizing Link-class blocks
        which reliably have source URLs.
        """
        if not self.contents:
            return None

        def has_source_url(block):
            """Check if block has a valid source URL."""
            source = block.get('source')
            return source is not None and source.get('url')

        # Filter for Link class blocks (most reliable for source URLs)
        link_blocks = [
            b for b in self.contents
            if b.get('class') == 'Link' and has_source_url(b)
        ]

        if link_blocks:
            block = random.choice(link_blocks)
            return block['source']['url']

        # Fallback: try any block with a source URL
        blocks_with_source = [
            b for b in self.contents
            if has_source_url(b)
        ]

        if blocks_with_source:
            block = random.choice(blocks_with_source)
            return block['source']['url']

        return None
