# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Moonjump is a Flask server that redirects users to random interesting pages from curated sources: Are.na channels, Hacker News, Marginalia Search, and Wikipedia. The frontend displays pages in an iframe with embedding checks.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py  # Runs on port 5000 with debug mode

# Production server
gunicorn -c guniorn_config.py app:app  # Runs on 0.0.0.0:8080
```

## Architecture

### Core Components

- **app.py** - Flask application with all routes. Main endpoint `/jump` returns JSON with URL and embedding status, using a fallback chain: SQLite database → Hacker News → Wikipedia
- **lib/db.py** - SQLite database layer for storing crawled sites. Uses a cached count for random selection. Marks sites as non-jumpable when they block iframe embedding
- **lib/arena.py** - Are.na API client. Uses weighted random selection across configured channels (weights based on page count)
- **lib/hn.py** - Hacker News Firebase API client. Randomly selects from top/best/new stories
- **lib/search.py** - Marginalia Search scraper for discovering obscure websites
- **lib/helpers.py** - Utility functions for weighted random selection

### Data Flow

1. `/jump` endpoint tries to serve a random HTTPS site from the local SQLite database (`lib/sites.db`)
2. Before returning, it checks if the site allows iframe embedding via `X-Frame-Options` and `Content-Security-Policy` headers
3. Non-embeddable sites are marked in the database and skipped on future requests
4. Fallback chain: Database → Hacker News → Wikipedia random

### Database

SQLite database at `lib/sites.db` with `sites` table:
- `source_url` - URL of the site
- `can_jump` - Boolean flag for iframe embeddability
- `last_checked` - Timestamp of last check

### Frontend

Static HTML/JS in `static/index.html` that fetches from `/jump` and displays the returned URL in an iframe.
