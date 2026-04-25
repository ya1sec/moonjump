import math
import os
import random
import time
from urllib.parse import parse_qs, urlparse

import requests


ARENA_API_BASE = "https://api.are.na/v3"
ARENA_TOKEN = os.environ.get("ARENA_TOKEN", "")
CHANNEL_PAGE_SIZE = 24
REQUEST_TIMEOUT = 8
META_CACHE_TTL = 60 * 10


class ArenaError(Exception):
    pass


# Seed channels stay intentionally broad. A jump is still random; these weights
# only shape the kind of web Moonjump tends to land in.
SEED_CHANNELS = [
    {"slug": "www-portfolios-and-studios", "title": "www.: Portfolios and Studios", "weight": 8, "fallback_pages": 94},
    {"slug": "internet-escape", "title": "internet escape", "weight": 7, "fallback_pages": 26},
    {"slug": "bookmarks-1ntdk32bur0", "title": "bookmarks", "weight": 6, "fallback_pages": 23},
    {"slug": "dev-tools-y8yzn_83uci", "title": "dev tools", "weight": 3, "fallback_pages": 105},
    {"slug": "we-should-talk-about-this-website", "title": "we should talk about this website", "weight": 4, "fallback_pages": 15},
    {"slug": "www-62v_kltr0d8", "title": "www.", "weight": 4, "fallback_pages": 13},
    {"slug": "site-cite-sight", "title": "Site, Cite, Sight", "weight": 3, "fallback_pages": 3},
    {"slug": "thirsty-for-knowledge", "title": "Thirsty for Knowledge", "weight": 3, "fallback_pages": 16},
    {"slug": "internet-surfing-clubs", "title": "internet surfing clubs", "weight": 3, "fallback_pages": 7},
    {"slug": "love-at-first-site", "title": "love at first site", "weight": 4, "fallback_pages": 31},
    {"slug": "coolsites-biz", "title": "* COOLSITES.BIZ", "weight": 4, "fallback_pages": 27},
    {"slug": "web-1524558860", "title": "web", "weight": 6, "fallback_pages": 159},
    {"slug": "dotcom-bd4vxf9rydi", "title": "DOTCOM", "weight": 4, "fallback_pages": 42},
    {"slug": "sexy_web", "title": "sexy_web", "weight": 3, "fallback_pages": 19},
]

CHANNEL_ALIASES = {
    "devtools": "dev-tools-y8yzn_83uci",
    "django": "django-7kobd_9biyi",
    "bookmarks": "bookmarks-1ntdk32bur0",
}

CHANNEL_BY_SLUG = {channel["slug"]: channel for channel in SEED_CHANNELS}

# Backward-compatible channel dictionary for older callers/docs.
channels = {
    channel["slug"]: channel["weight"]
    for channel in SEED_CHANNELS
}

_channel_meta_cache = {}


def _headers():
    headers = {
        "Accept": "application/json",
        "User-Agent": "Moonjump/1.0 (+https://moonjump.app)",
    }
    if ARENA_TOKEN:
        headers["Authorization"] = f"Bearer {ARENA_TOKEN}"
    return headers


def _get(path, params=None):
    url = f"{ARENA_API_BASE}{path}"
    try:
        response = requests.get(
            url,
            params=params or {},
            headers=_headers(),
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise ArenaError(str(exc)) from exc

    if not response.ok:
        raise ArenaError(f"Are.na request failed: {response.status_code}")

    try:
        return response.json()
    except ValueError as exc:
        raise ArenaError("Are.na returned invalid JSON") from exc


def _weighted_choice(items):
    total = sum(item.get("weight", 1) for item in items)
    cursor = random.uniform(0, total)
    for item in items:
        cursor -= item.get("weight", 1)
        if cursor <= 0:
            return item
    return items[-1]


def _split_channel(channel):
    if not channel:
        return None, None

    if channel in CHANNEL_ALIASES:
        return CHANNEL_ALIASES[channel], None

    parsed = urlparse(channel)
    if parsed.query:
        page = parse_qs(parsed.query).get("page", [None])[0]
        return parsed.path or channel.split("?")[0], int(page) if page and page.isdigit() else None

    if "?page=" in channel:
        slug, page = channel.split("?page=", 1)
        return slug, int(page) if page.isdigit() else None

    return channel, None


def _text(value):
    if not value:
        return None
    if isinstance(value, str):
        return value
    return value.get("plain") or value.get("markdown")


def _image_url(image):
    if not image:
        return None
    for key in ("medium", "large", "display", "small", "thumb", "original"):
        size = image.get(key) or {}
        if size.get("src") or size.get("url"):
            return size.get("src") or size.get("url")
    return image.get("src")


def _user_name(user):
    if not user:
        return None
    return user.get("name") or user.get("username") or user.get("slug")


def _normalize_channel(channel):
    owner = channel.get("owner") or channel.get("user") or {}
    counts = channel.get("counts") or {}
    return {
        "id": channel.get("id"),
        "slug": channel.get("slug") or str(channel.get("id")),
        "title": channel.get("title") or "Untitled channel",
        "visibility": channel.get("visibility") or channel.get("status") or "public",
        "length": channel.get("length") or counts.get("contents") or counts.get("blocks") or 0,
        "owner": _user_name(owner),
        "owner_slug": owner.get("slug"),
    }


def _normalize_block(block, channel=None):
    source = block.get("source") or {}
    owner = block.get("user") or block.get("owner") or {}
    connected_by = (block.get("connection") or {}).get("connected_by") or owner
    counts = block.get("counts") or {}
    block_type = block.get("type") or block.get("class") or "Block"
    url = source.get("url")

    return {
        "id": block.get("id"),
        "type": block_type,
        "url": url,
        "source": {
            "url": url,
            "title": source.get("title") or block.get("title"),
        } if url else None,
        "title": source.get("title") or block.get("title") or _text(block.get("content")) or "Untitled",
        "description": _text(block.get("description")),
        "content": _text(block.get("content")),
        "image_url": _image_url(block.get("image")),
        "curator": _user_name(connected_by),
        "curator_slug": connected_by.get("slug") if connected_by else None,
        "connected_at": (block.get("connection") or {}).get("connected_at") or block.get("connected_at"),
        "connection_count": (
            block.get("connection_count")
            or counts.get("connections")
            or counts.get("channels")
            or 0
        ),
        "channel": channel or {},
        "source_kind": "arena:v3",
    }


def _channel_meta(slug):
    now = time.time()
    cached = _channel_meta_cache.get(slug)
    if cached and now - cached["cached_at"] < META_CACHE_TTL:
        return cached["meta"]

    data = _get(f"/channels/{slug}")
    meta = _normalize_channel(data)
    _channel_meta_cache[slug] = {
        "cached_at": now,
        "meta": meta,
    }
    return meta


def _channel_total_pages(slug):
    seed = CHANNEL_BY_SLUG.get(slug, {})
    fallback = max(1, seed.get("fallback_pages", 1))
    try:
        length = int(_channel_meta(slug).get("length") or 0)
    except (ArenaError, TypeError, ValueError):
        return fallback

    if length <= 0:
        return fallback
    return max(1, math.ceil(length / CHANNEL_PAGE_SIZE))


def get_channel(channel):
    slug, page = _split_channel(channel)
    if not slug:
        seed = _weighted_choice(SEED_CHANNELS)
        slug = seed["slug"]

    page = page or random.randint(1, _channel_total_pages(slug))
    params = {"page": page, "per": CHANNEL_PAGE_SIZE}
    data = _get(f"/channels/{slug}/contents", params=params)
    raw_items = data.get("data") or []

    channel_meta = CHANNEL_BY_SLUG.get(slug)
    if not channel_meta:
        try:
            channel_meta = _channel_meta(slug)
        except ArenaError:
            channel_meta = {"slug": slug, "title": slug}

    contents = [
        _normalize_block(item, channel_meta)
        for item in raw_items
        if (item.get("type") or item.get("class")) != "Channel"
    ]
    return contents, len(contents)


class Arena:
    def __init__(self, channel=None):
        slug, page = _split_channel(channel)
        if slug:
            self.channel = slug
            self.page = page
        else:
            seed = _weighted_choice(SEED_CHANNELS)
            self.channel = seed["slug"]
            self.page = None

        self.contents = []
        self.length = 0

    def get_channel_contents(self):
        self.contents, self.length = get_channel(
            f"{self.channel}?page={self.page}" if self.page else self.channel
        )
        return self.contents

    def get_item(self):
        if not self.contents:
            self.get_channel_contents()

        candidates = [
            item for item in self.contents
            if item.get("url") and item["url"].startswith("https://")
        ]
        if not candidates:
            raise ArenaError("No usable links found in channel page")
        return random.choice(candidates)

    def get_item_url(self):
        return self.get_item()["url"]

    def random_from_channel(self, slug):
        last_error = None
        for _ in range(4):
            try:
                self.channel = slug
                self.page = random.randint(1, _channel_total_pages(slug))
                self.get_channel_contents()
                return self.get_item()
            except ArenaError as exc:
                last_error = exc

        raise last_error or ArenaError("No random item found")

    def random_jump(self, channel_slug=None):
        if channel_slug:
            slug, _ = _split_channel(channel_slug)
            return self.random_from_channel(slug)

        last_error = None
        for _ in range(6):
            seed = _weighted_choice(SEED_CHANNELS)
            try:
                return self.random_from_channel(seed["slug"])
            except ArenaError as exc:
                last_error = exc

        raise last_error or ArenaError("Are.na random jump failed")

    def drift_jump(self, block_id):
        if not block_id:
            return self.random_jump()

        data = _get(
            f"/blocks/{block_id}/connections",
            params={"page": 1, "per": 50},
        )
        channels = [
            _normalize_channel(channel)
            for channel in data.get("data", [])
            if channel.get("visibility") != "private"
        ]
        channels = [channel for channel in channels if channel.get("slug")]

        if not channels:
            return self.random_jump()

        channel = random.choice(channels)
        return self.random_from_channel(channel["slug"])

    def get_jump(self, mode="random", channel_slug=None, block_id=None):
        if mode == "same_channel" and channel_slug:
            return self.random_jump(channel_slug=channel_slug)
        if mode == "drift":
            return self.drift_jump(block_id)
        return self.random_jump()
