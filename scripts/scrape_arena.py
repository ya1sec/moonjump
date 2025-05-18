#%%
import csv
import requests
import tldextract

def dump_arena_links_to_csv(csv_filename='arena_sites.csv'):
    """
    Loops through every page of each channel and dumps link metadata to a CSV file.

    CSV columns match the block schema from Are.na with the following modifications:
      - "source" fields flattened to source_url, source_title, source_provider_name, source_provider_url
      - "image" fields flattened similarly
      - "domain" extracted from the block's source_url (e.g. "example.com")
      - channel_name and channel_id added for context
    """

    # Channels and their maximum page counts (update as needed)
    channel_pages = {
        'love-at-first-site': None,
        'dev-tools-y8yzn_83uci': None,
        'bookmarks-1ntdk32bur0': None,
        'sexy_web': None,
        'web-1524558860': None,
        'dotcom-bd4vxf9rydi': None,
        'coolsites-biz': None,
        'www-portfolios-and-studios': None,  # Set to None to fetch all pages
        'internet-escape': None,
        'we-should-talk-about-this-website': None,
        'www-62v_kltr0d8': None,
        'site-cite-sight': None,
        'thirsty-for-knowledge': None,
        'internet-surfing-clubs': None,
        # Add more channels here if desired
    }

    # Define the CSV columns
    columns = [
        'id',
        'title',
        'updated_at',
        'created_at',
        'state',
        'comment_count',
        'generated_title',
        'content_html',
        'description_html',
        'visibility',
        'content',
        'description',

        # Flattened source fields
        'source_url',
        'source_title',
        'source_provider_name',
        'source_provider_url',

        # Flattened image fields
        'image_filename',
        'image_content_type',
        'image_updated_at',
        'image_thumb_url',
        'image_square_url',
        'image_display_url',
        'image_large_url',
        'image_original_url',
        'image_original_file_size',

        'embed',
        'attachment',
        'metadata',
        'base_class',
        'class',

        # user fields flattened
        'user_id',
        'user_created_at',
        'user_slug',
        'user_username',
        'user_first_name',
        'user_last_name',
        'user_full_name',
        'user_avatar',
        'user_channel_count',
        'user_following_count',
        'user_profile_id',
        'user_follower_count',
        'user_initials',
        'user_can_index',
        'user_metadata_description',
        'user_is_premium',
        'user_is_lifetime_premium',
        'user_is_supporter',
        'user_is_exceeding_connections_limit',
        'user_is_confirmed',
        'user_is_pending_reconfirmation',
        'user_is_pending_confirmation',
        'user_badge',
        'user_base_class',
        'user_class',

        'position',
        'selected',
        'connection_id',
        'connected_at',
        'connected_by_user_id',
        'connected_by_username',
        'connected_by_user_slug',

        # Our custom additions:
        'channel_name',
        'channel_id',
        'domain',  # e.g. "example.com"
    ]

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        # Loop through each channel and each page
        for channel_slug in channel_pages.keys():
            page_num = 1  # Start from the first page
            while True:  # Continue fetching until no more pages
                print(f"Fetching {channel_slug} page {page_num}...")
                arena_url = f'https://api.are.na/v2/channels/{channel_slug}?page={page_num}&per=1000'
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                    resp = requests.get(arena_url, headers=headers, timeout=10)
                    if not resp.ok:
                        print(f"Request failed for {arena_url} [{resp.status_code}]")
                        print(resp.text)
                        break  # Exit the loop on failure

                    data = resp.json()

                    # Check if there are contents to process
                    contents = data.get('contents', [])
                    if not contents:
                        print(f"No more contents found for {channel_slug}.")
                        break  # Exit the loop if no contents are returned

                    # channel info
                    channel_id = data.get('id')
                    channel_name = data.get('title')

                    for block in contents:
                        # Skip blocks that don't have a link
                        source_dict = block.get('source') or {}
                        link_url = source_dict.get('url')
                        if not link_url:
                            continue

                        row = {}

                        # Top-level block fields
                        row['id'] = block.get('id')
                        row['title'] = block.get('title')
                        row['updated_at'] = block.get('updated_at')
                        row['created_at'] = block.get('created_at')
                        row['state'] = block.get('state')
                        row['comment_count'] = block.get('comment_count')
                        row['generated_title'] = block.get('generated_title')
                        row['content_html'] = block.get('content_html')
                        row['description_html'] = block.get('description_html')
                        row['visibility'] = block.get('visibility')
                        row['content'] = block.get('content')
                        row['description'] = block.get('description')
                        row['embed'] = block.get('embed')
                        row['attachment'] = block.get('attachment')
                        row['metadata'] = block.get('metadata')
                        row['base_class'] = block.get('base_class')
                        row['class'] = block.get('class')
                        row['position'] = block.get('position')
                        row['selected'] = block.get('selected')
                        row['connection_id'] = block.get('connection_id')
                        row['connected_at'] = block.get('connected_at')
                        row['connected_by_user_id'] = block.get('connected_by_user_id')
                        row['connected_by_username'] = block.get('connected_by_username')
                        row['connected_by_user_slug'] = block.get('connected_by_user_slug')

                        # Flatten the source sub-dict
                        row['source_url'] = link_url
                        row['source_title'] = source_dict.get('title')
                        provider = source_dict.get('provider') or {}
                        row['source_provider_name'] = provider.get('name')
                        row['source_provider_url'] = provider.get('url')

                        # Flatten the image sub-dict
                        image_dict = block.get('image') or {}
                        row['image_filename'] = image_dict.get('filename')
                        row['image_content_type'] = image_dict.get('content_type')
                        row['image_updated_at'] = image_dict.get('updated_at')

                        thumb = image_dict.get('thumb') or {}
                        row['image_thumb_url'] = thumb.get('url')

                        square = image_dict.get('square') or {}
                        row['image_square_url'] = square.get('url')

                        display = image_dict.get('display') or {}
                        row['image_display_url'] = display.get('url')

                        large = image_dict.get('large') or {}
                        row['image_large_url'] = large.get('url')

                        original = image_dict.get('original') or {}
                        row['image_original_url'] = original.get('url')
                        row['image_original_file_size'] = original.get('file_size')

                        # Flatten the user sub-dict
                        user = block.get('user') or {}
                        row['user_id'] = user.get('id')
                        row['user_created_at'] = user.get('created_at')
                        row['user_slug'] = user.get('slug')
                        row['user_username'] = user.get('username')
                        row['user_first_name'] = user.get('first_name')
                        row['user_last_name'] = user.get('last_name')
                        row['user_full_name'] = user.get('full_name')
                        row['user_avatar'] = user.get('avatar')
                        row['user_channel_count'] = user.get('channel_count')
                        row['user_following_count'] = user.get('following_count')
                        row['user_profile_id'] = user.get('profile_id')
                        row['user_follower_count'] = user.get('follower_count')
                        row['user_initials'] = user.get('initials')
                        row['user_can_index'] = user.get('can_index')

                        user_metadata = user.get('metadata') or {}
                        row['user_metadata_description'] = user_metadata.get('description')
                        row['user_is_premium'] = user.get('is_premium')
                        row['user_is_lifetime_premium'] = user.get('is_lifetime_premium')
                        row['user_is_supporter'] = user.get('is_supporter')
                        row['user_is_exceeding_connections_limit'] = user.get('is_exceeding_connections_limit')
                        row['user_is_confirmed'] = user.get('is_confirmed')
                        row['user_is_pending_reconfirmation'] = user.get('is_pending_reconfirmation')
                        row['user_is_pending_confirmation'] = user.get('is_pending_confirmation')
                        row['user_badge'] = user.get('badge')
                        row['user_base_class'] = user.get('base_class')
                        row['user_class'] = user.get('class')

                        # Channel info
                        row['channel_id'] = channel_id
                        row['channel_name'] = channel_name

                        # Extract domain (registered domain) from the link
                        parsed = tldextract.extract(link_url)
                        row['domain'] = parsed.registered_domain

                        # Finally, write the row
                        writer.writerow(row)

                    page_num += 1  # Move to the next page

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching {arena_url}: {e}")
                    break  # Exit the loop on error

    print(f"\nDone! CSV saved to '{csv_filename}'.")

#%%
dump_arena_links_to_csv()	

# #%%
# # Remove any duplicate ids in the csv
# import pandas as pd
# df = pd.read_csv('arena_sites.csv')
# df = df.drop_duplicates(subset='id', keep='first')
# df.to_csv('arena_sites.csv', index=False)

# #%%
# def check_iframable(url, blocking_phrases=None, timeout=5):
#     """
#     Returns (can_jump, reason).
#     can_jump is True if the site is embeddable in an <iframe>,
#     False otherwise.

#     reason is a short string explaining why it fails or "OK" if it is embeddable.
#     """
#     if blocking_phrases is None:
#         blocking_phrases = [
#             'blocked by chromium',
#             'security error',
#             'cannot be displayed in a frame',
#             'x-frame-options',
#             'refused to connect'
#         ]

#     try:
#         print(f"Checking {url}...")
#         # HEAD request first to check if the site is up and not blocking framing
#         head_resp = requests.head(url, allow_redirects=True, timeout=timeout)

#         if not head_resp.ok:
#             return False, f"HEAD status: {head_resp.status_code}"

#         # Check X-Frame-Options and Content-Security-Policy
#         xfo = head_resp.headers.get('X-Frame-Options', '').upper()
#         csp = head_resp.headers.get('Content-Security-Policy', '')

#         # Many sites block framing via 'DENY' or 'SAMEORIGIN' or 'frame-ancestors'
#         if xfo in ['DENY', 'SAMEORIGIN'] or 'frame-ancestors' in csp or 'X-Frame-Options' in csp:
#             return False, f"Blocked by X-Frame / CSP: xfo={xfo}, csp={csp}"

#         # If HEAD looks good, do a GET to see if the content is actually loadable
#         get_resp = requests.get(url, timeout=timeout)

#         if not get_resp.ok:
#             return False, f"GET status: {get_resp.status_code}"

#         # Look for any suspicious phrases in the HTML that often imply refusal
#         content_lower = get_resp.text.lower()
#         for phrase in blocking_phrases:
#             if phrase in content_lower:
#                 return False, f"Blocking phrase '{phrase}' found in content"

#         # If we made it here, it should be embeddable
#         return True, "OK"

#     except (requests.exceptions.ConnectionError,
#             requests.exceptions.SSLError,
#             requests.exceptions.TooManyRedirects,
#             requests.exceptions.RequestException,
#             requests.exceptions.Timeout) as e:
#         return False, f"Request error: {str(e)}"


# def add_iframable_info_to_csv(input_csv='arena_sites.csv', output_csv='arena_sites_checked.csv'):
#     with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
#          open(output_csv, 'w', newline='', encoding='utf-8') as outfile:

#         reader = csv.DictReader(infile)
#         fieldnames = reader.fieldnames + ['can_jump', 'jump_block_reason']

#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#         writer.writeheader()

#         for row in reader:
#             url = row.get('source_url')  # or whichever column holds the link
#             if not url:
#                 row['can_jump'] = False
#                 row['jump_block_reason'] = "No URL"
#             else:
#                 can_jump, reason = check_iframable(url)
#                 row['can_jump'] = can_jump
#                 row['jump_block_reason'] = reason

#             writer.writerow(row)

#     print(f"Done! Wrote updated rows to {output_csv}.")

# #%%
# add_iframable_info_to_csv()
