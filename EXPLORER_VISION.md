# Moonjump Explorer Vision

> Reimagining Moonjump as a rich exploration platform for the curated web.

## Table of Contents

- [Current State Analysis](#current-state-analysis)
- [The Are.na API Opportunity](#the-arena-api-opportunity)
- [Exploration Dimensions](#exploration-dimensions)
- [Feature Concepts](#feature-concepts)
- [UI/UX Patterns](#uiux-patterns)
- [Existing Ecosystem](#existing-ecosystem)
- [Architecture Recommendations](#architecture-recommendations)
- [Implementation Roadmap](#implementation-roadmap)
- [References](#references)

---

## Current State Analysis

### What Moonjump Does Today

Moonjump is a "random jump" server that redirects users to interesting pages from curated sources:

```
User clicks "Jump"
    → Server picks random channel (weighted)
    → Fetches random page from channel
    → Picks random Link block
    → Extracts source URL
    → Returns URL for iframe display
```

### Data Flow

1. **Channels**: Hardcoded dictionary with weights in `lib/arena.py`
2. **Selection**: Weighted random channel → random page → random block
3. **Filtering**: Only `Link` class blocks with valid `source.url`
4. **Validation**: HEAD request to check iframe embedding headers
5. **Fallback**: Database → Hacker News → Wikipedia

### What We're Missing

| Available in API | Currently Used | Potential |
|------------------|----------------|-----------|
| Block title | ❌ | Context before jumping |
| Block description | ❌ | Richer previews |
| Block thumbnail | ❌ | Visual discovery |
| Block connections | ❌ | Rabbit hole navigation |
| Channel metadata | ❌ | Source attribution |
| Channel connections | ❌ | Related exploration |
| Text blocks | ❌ | Inline reading mode |
| Image blocks | ❌ | Gallery mode |
| Search API | ❌ | User-driven discovery |

**Core insight**: We're flattening a rich graph structure into a random URL dispenser.

---

## The Are.na API Opportunity

### Block Attributes

Every block contains rich metadata we can surface:

```json
{
  "id": 12345,
  "title": "Strange Horizons - Speculative Fiction",
  "description": "An underrated magazine with amazing short stories...",
  "class": "Link",
  "source": {
    "url": "https://strangehorizons.com",
    "provider": {
      "name": "strangehorizons.com",
      "url": "https://strangehorizons.com"
    }
  },
  "image": {
    "thumb": { "url": "https://..." },
    "display": { "url": "https://..." },
    "original": { "url": "https://..." }
  },
  "user": {
    "slug": "username",
    "full_name": "User Name"
  },
  "connections": [
    { "id": 111, "title": "Literary Magazines", "slug": "literary-magazines" },
    { "id": 222, "title": "Speculative Fiction", "slug": "speculative-fiction" }
  ]
}
```

### Block Types

| Type | Content | Exploration Use |
|------|---------|-----------------|
| **Link** | URL with screenshot | Current behavior (jump to URL) |
| **Text** | Markdown content | Quotes, notes, poems—display inline |
| **Image** | Uploaded/saved images | Visual gallery mode |
| **Media** | Embeds (YouTube, Vimeo) | Embedded media viewing |
| **Attachment** | PDFs, files | Document exploration |

### Key Endpoints

| Endpoint | Purpose | New Feature |
|----------|---------|-------------|
| `GET /channels/:slug` | Full channel metadata | Channel info display |
| `GET /channels/:id/contents` | Paginated blocks | Browse within channel |
| `GET /channels/:id/thumb` | First 9 blocks | Quick channel preview |
| `GET /channels/:id/connections` | Connected channels | Spider between channels |
| `GET /channels/:id/channels` | All connected channels | Graph visualization |
| `GET /blocks/:id` | Full block metadata | Rich previews |
| `GET /blocks/:id/channels` | Channels containing block | Rabbit hole navigation |
| `GET /search/channels?q=` | Search channels | User finds new channels |
| `GET /search/blocks?q=` | Search blocks | Content discovery |

---

## Exploration Dimensions

### 1. Block Connections as Navigation

Every block exists in **multiple channels**. When a user lands on something interesting:

```
┌─────────────────────────────────────────┐
│  You're viewing: "Strange Horizons"     │
│                                         │
│  This also appears in:                  │
│  • Literary Magazines (234 blocks)      │
│  • Speculative Fiction (89 blocks)      │
│  • Web Zines (156 blocks)               │
│                                         │
│  [Explore Literary Magazines →]         │
└─────────────────────────────────────────┘
```

This creates **rabbit holes**—organic pathways through the graph.

### 2. Channel Connections (Spider Mode)

Channels connect to other channels through shared blocks:

```
         ┌─────────────┐
         │  Internet   │
         │   Escape    │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌───────┐  ┌───────┐  ┌───────┐
│ 90s   │  │ Weird │  │ Web   │
│ Web   │  │ Sites │  │ Art   │
└───────┘  └───────┘  └───────┘
```

Users can "drift" between related channels based on connections.

### 3. Metadata-Rich Display

Instead of jumping blind, show context:

```
┌─────────────────────────────────────────┐
│ ┌─────────────────────────────────────┐ │
│ │                                     │ │
│ │     [Screenshot/Thumbnail]          │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ "Strange Horizons - Fiction Issue"      │
│ strangehorizons.com                     │
│                                         │
│ from channel: Literary Magazines        │
│ saved by: @curator_name                 │
│                                         │
│ "An underrated speculative fiction      │
│  magazine with amazing short stories    │
│  and poetry. Updated weekly."           │
│                                         │
│ [Jump] [Skip] [Save] [Explore Channel]  │
└─────────────────────────────────────────┘
```

### 4. Multi-Modal Exploration

Different content types, different experiences:

| Mode | Content | Interface |
|------|---------|-----------|
| **Links** (current) | URLs | Iframe embed |
| **Gallery** | Images | Thumbnail grid, lightbox |
| **Reading** | Text blocks | Inline markdown display |
| **Media** | Videos/embeds | Embedded player |
| **Mixed** | Random type | Surprise me |

### 5. User-Curated Channels

Let users build their own exploration pools:

```
┌─────────────────────────────────────────┐
│ Your Channels                           │
│                                         │
│ ✓ Internet Escape (default)             │
│ ✓ WWW Portfolios (default)              │
│ ✓ Dev Tools (default)                   │
│ + brutalist-websites (added by you)     │
│ + generative-art (added by you)         │
│                                         │
│ [Search Are.na for more channels...]    │
└─────────────────────────────────────────┘
```

---

## Feature Concepts

### Tier 1: Quick Wins (Enhance Current Flow)

#### 1.1 Block Preview Card

Show metadata before jumping:

- Thumbnail image
- Title and description
- Source domain
- Channel name
- Curator attribution

**API**: Use existing block data from `/channels/:slug/contents`

#### 1.2 Skip Button

Don't like what you see? Get another instantly without closing the iframe.

**Implementation**: Frontend fetches next random block, swaps preview card.

#### 1.3 Channel Attribution

Always show: "from: [Channel Name]"

Click to browse that channel.

#### 1.4 History Breadcrumbs

```
Home → Internet Escape → [current block] → ...
     ← Literary Magazines ←
```

- Last 5-10 visited items
- Click to revisit
- localStorage persistence

---

### Tier 2: Rabbit Hole Mode

#### 2.1 "See Connections"

After landing on a block, overlay shows other channels containing it:

```javascript
// Fetch connections
GET /v2/blocks/:id/channels

// Display
"This also appears in 7 channels"
→ Click to see list
→ Click channel to explore it
```

#### 2.2 Channel Spider

"Explore related channels" button:

```javascript
// Fetch connected channels
GET /v2/channels/:id/channels

// Display 3-5 related channels with thumbnails
// User clicks one → new exploration context
```

#### 2.3 Exploration Path Tracking

Visual trail of the journey:

```
[Start] → Channel A → Block 1 → Channel B → Block 2 → [You are here]
                                    ↑
                              [Backtrack]
```

---

### Tier 3: User Curation

#### 3.1 Add Your Own Channels

Search interface for Are.na channels:

```javascript
// User searches
GET /v2/search/channels?q=brutalist+web

// Results displayed
// User clicks "Add to my pool"
// Stored in localStorage
```

#### 3.2 Category/Mood Modes

Pre-defined categories for exploration mood:

```javascript
const CATEGORIES = {
  'weird-web': ['internet-escape', 'site-cite-sight', 'www-62v_kltr0d8'],
  'tools': ['dev-tools-y8yzn_83uci', 'bookmarks-1ntdk32bur0'],
  'knowledge': ['thirsty-for-knowledge'],
  'visual': ['www-portfolios-and-studios'],
};
```

UI: "I want to explore... [Weird Web] [Tools] [Knowledge] [Visual] [Everything]"

#### 3.3 Favorites & Blacklist

- **Save**: Add interesting finds to a favorites list
- **Blacklist**: Never show this domain again
- **Export**: Share your favorites as a list

---

### Tier 4: Visual Modes

#### 4.1 Gallery Mode

For channels rich in images:

```
┌─────┬─────┬─────┬─────┐
│     │     │     │     │
│ img │ img │ img │ img │
│     │     │     │     │
├─────┼─────┼─────┼─────┤
│     │     │     │     │
│ img │ img │ img │ img │
│     │     │     │     │
└─────┴─────┴─────┴─────┘
```

- Click to expand/view full size
- Infinite scroll pagination
- Filter: `block.class === 'Image'`

#### 4.2 Reading Mode

For text blocks (quotes, notes, excerpts):

```
┌─────────────────────────────────────────┐
│                                         │
│  "The street finds its own uses for     │
│   things."                              │
│                                         │
│   — William Gibson                      │
│                                         │
│  from: Cyberpunk Quotes                 │
│                                         │
│  [Next Quote] [Save] [Explore Channel]  │
└─────────────────────────────────────────┘
```

- Render `content_html` or `content` (markdown)
- Filter: `block.class === 'Text'`

#### 4.3 Mixed Media Mode

Randomly serve any block type:

- Link → iframe/preview
- Image → lightbox
- Text → inline display
- Media → embedded player

Each jump is a surprise format.

---

### Tier 5: Advanced Features (Future)

#### 5.1 Mini Graph View

Interactive D3 force graph of channel connections:

```
        ○ Channel A
       /|\
      / | \
     ○  ○  ○
    /|  |  |\
   ○ ○  ○  ○ ○
```

- Nodes = channels
- Edges = shared blocks
- Click node to explore
- Zoom/pan navigation

#### 5.2 Session Sharing

Generate shareable URL of exploration path:

```
moonjump.app/journey/abc123

"Here's the weird path I took through the web..."

1. Started at: Internet Escape
2. Found: Strange Horizons
3. Rabbit-holed to: Literary Magazines
4. Discovered: Clarkesworld
...
```

#### 5.3 Serendipity Dial

Control the randomness:

```
[Deep Random]←───────────────→[Guided]
     │                            │
     │  ● Current setting         │
     │                            │
  Any channel              Stay in topic
  Any block                Follow connections
  Pure chaos               Thematic drift
```

---

## UI/UX Patterns

### Discovery UI Inspirations

| Pattern | Source | Application |
|---------|--------|-------------|
| **Swipe navigation** | Tinder | Left=skip, Right=explore more |
| **Card preview** | Pinterest | Metadata card before commitment |
| **Breadcrumb trail** | Wikipedia | "You came from → here → here" |
| **Related items** | Netflix | "Because you explored X, try Y" |
| **Infinite canvas** | Miro/Figma | Spatial exploration of blocks |
| **Force graph** | D3 examples | Visual channel connections |

### StumbleUpon Successors

| Tool | Pattern | Takeaway |
|------|---------|----------|
| **Cloudhiker** | Categories + thumbs up/down | Feedback improves selection |
| **The Useless Web** | Pure random, no context | Too minimal—no rabbit holes |
| **Wiby.me** | Curated "old web" index | Similar curation philosophy |
| **Marginalia** | Random + site preview | Already integrated |

### Key Principles

1. **Progressive disclosure**: Show just enough, reveal more on demand
2. **Low commitment**: Easy to skip, easy to backtrack
3. **Contextual richness**: Every jump has meaning/attribution
4. **Rabbit hole support**: Easy to follow tangents
5. **Personal curation**: Users shape their exploration space

---

## Existing Ecosystem

### Are.na Tools (Reference Projects)

#### Graph/Network Visualization

| Project | Description | Relevance |
|---------|-------------|-----------|
| [arena-connectome](https://github.com/nicschumann/arena-connectome) | Graph structure analysis, n-neighborhood visualization | Graph algorithms, connection traversal |
| [spider](https://github.com/hxrts/spider) | Crawls connected channels, visualizes network | Spidering logic |
| [arena-graph](https://github.com/kees-/arena-graph) | D3 force graph in ClojureScript | Frontend graph viz |

#### Interactive Explorers

| Project | Description | Relevance |
|---------|-------------|-----------|
| [arena-explorer](https://github.com/merryvj/arena-explorer) | React canvas with pan/zoom | Interactive block display |
| [are.na-multiplexer](https://github.com/mguidetti/are.na-multiplexer) | Tiling window manager (76★) | Multi-channel viewing |
| [groves](https://github.com/devinhalladay/groves) | Alternative organization paradigm | Beyond-channel thinking |

#### API Clients

| Project | Description | Relevance |
|---------|-------------|-----------|
| [ervell](https://github.com/aredotna/ervell) | Official Are.na frontend (200★) | Reference implementation |
| [arena-ts](https://github.com/e-e-e/arena-ts) | TypeScript client (38★) | Type definitions |
| [arena (Python)](https://github.com/frnsys/arena) | Python API wrapper | Backend integration |

### Moonjump's Unique Position

| Existing Tool | Purpose | Moonjump's Angle |
|---------------|---------|------------------|
| ervell | Manage your Are.na | Explore **others'** Are.na |
| arena-connectome | Analyze structure | **Play** in the structure |
| are.na-multiplexer | Power user productivity | **Casual serendipity** |
| StumbleUpon clones | Generic random | **Curated sources** |

**Unique value**: Curated randomness from high-quality sources, with just enough context to make exploration meaningful without overwhelming.

---

## Architecture Recommendations

### Current API

```python
# What we return now
@app.route('/jump')
def jump():
    # ... selection logic ...
    return jsonify({"url": link, "can_embed": True})
```

### Enhanced API

```python
# New endpoints

@app.route('/api/random-block')
def random_block():
    """Returns full block metadata for preview."""
    return jsonify({
        "block": {
            "id": 12345,
            "title": "Strange Horizons",
            "description": "Amazing speculative fiction magazine",
            "type": "Link",
            "source_url": "https://strangehorizons.com",
            "source_domain": "strangehorizons.com",
            "thumbnail": "https://d2w9rnfcy7mm78.cloudfront.net/...",
            "channel": {
                "slug": "literary-magazines",
                "title": "Literary Magazines",
                "length": 234
            },
            "connected_channels_count": 7
        },
        "can_embed": True
    })

@app.route('/api/channel/<slug>')
def get_channel(slug):
    """Returns channel info with preview blocks."""
    return jsonify({
        "channel": {
            "slug": slug,
            "title": "Literary Magazines",
            "description": "...",
            "length": 234,
            "preview_blocks": [...]  # First 9 blocks
        }
    })

@app.route('/api/block/<int:block_id>/connections')
def block_connections(block_id):
    """Returns channels containing this block."""
    return jsonify({
        "block_id": block_id,
        "channels": [
            {"slug": "...", "title": "...", "length": 123},
            ...
        ]
    })

@app.route('/api/search/channels')
def search_channels():
    """Search Are.na for channels."""
    query = request.args.get('q', '')
    # Proxy to Are.na search API
    return jsonify({
        "query": query,
        "channels": [...]
    })
```

### Frontend Architecture

```
Current:
  Click "Jump" → fetch /jump → load iframe

Enhanced:
  Click "Jump"
      → fetch /api/random-block
      → display preview card
      → user clicks [Jump] → load iframe
      → user clicks [Skip] → fetch another
      → user clicks [Explore] → channel browse mode
      → user clicks [Connections] → rabbit hole mode
```

### Data Storage

```javascript
// localStorage structure
{
  "moonjump": {
    "userChannels": ["slug-1", "slug-2"],
    "favorites": [
      { "url": "...", "title": "...", "savedAt": "..." }
    ],
    "blacklist": ["domain1.com", "domain2.com"],
    "history": [
      { "blockId": 123, "channelSlug": "...", "timestamp": "..." }
    ],
    "preferences": {
      "mode": "mixed",  // links | gallery | reading | mixed
      "category": "all" // weird-web | tools | knowledge | all
    }
  }
}
```

### Caching Strategy

```python
# Cache channel metadata aggressively
# Are.na API is generous but respect it

CACHE_TTL = {
    'channel_metadata': 3600,      # 1 hour
    'channel_contents': 300,       # 5 minutes
    'block_connections': 3600,     # 1 hour
    'search_results': 60           # 1 minute
}
```

---

## Implementation Roadmap

### Phase 1: Enhanced Random (1-2 days)

**Goal**: Richer preview before jumping

- [ ] Modify `/jump` to return full block metadata
- [ ] Frontend: Display preview card (thumbnail, title, domain, channel)
- [ ] Add [Skip] button to get another random block
- [ ] Show "from: [Channel Name]" attribution
- [ ] Basic localStorage history (last 10 visits)

**API Changes**:
```python
# Return more data
return jsonify({
    "block": {
        "title": block.get('title'),
        "description": block.get('description'),
        "source_url": source_url,
        "source_domain": urlparse(source_url).netloc,
        "thumbnail": block.get('image', {}).get('display', {}).get('url'),
        "channel_title": channel_title,
        "channel_slug": channel_slug
    },
    "can_embed": headers_allow_embedding
})
```

### Phase 2: Rabbit Holes (3-5 days)

**Goal**: Follow connections between blocks and channels

- [ ] New endpoint: `/api/block/<id>/connections`
- [ ] Frontend: "Also appears in..." overlay
- [ ] Click channel to explore it
- [ ] Breadcrumb trail of exploration path
- [ ] Backtrack functionality

**New Code**:
```python
@app.route('/api/block/<int:block_id>/connections')
def block_connections(block_id):
    url = f'https://api.are.na/v2/blocks/{block_id}/channels'
    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.ok:
        data = response.json()
        channels = [
            {'slug': c['slug'], 'title': c['title'], 'length': c['length']}
            for c in data.get('channels', [])
        ]
        return jsonify({'channels': channels})
    return jsonify({'channels': []})
```

### Phase 3: User Curation (1 week)

**Goal**: Users can customize their exploration pool

- [ ] New endpoint: `/api/search/channels?q=`
- [ ] Frontend: Search modal for finding channels
- [ ] "Add to my pool" button
- [ ] localStorage persistence of user channels
- [ ] Category/mood filtering UI
- [ ] Favorites and blacklist

### Phase 4: Visual Modes (1 week)

**Goal**: Explore beyond links

- [ ] Gallery mode for image blocks
- [ ] Reading mode for text blocks
- [ ] Mode toggle in UI
- [ ] Filter blocks by type in backend

### Phase 5: Advanced Features (Stretch)

**Goal**: Deeper exploration tools

- [ ] Mini graph visualization (D3.js)
- [ ] Session sharing (shareable exploration paths)
- [ ] Serendipity dial (control randomness level)

---

## References

### Are.na API Documentation

- [Channels API](https://dev.are.na/documentation/channels)
- [Blocks API](https://dev.are.na/documentation/blocks)
- [Search API](https://dev.are.na/documentation/search)
- [Authentication](https://dev.are.na/documentation/authentication)

### Related Projects

- [arena-connectome](https://github.com/nicschumann/arena-connectome) - Graph visualization
- [are.na-multiplexer](https://github.com/mguidetti/are.na-multiplexer) - Tiling explorer
- [ervell](https://github.com/aredotna/ervell) - Official frontend
- [arena-ts](https://github.com/e-e-e/arena-ts) - TypeScript client

### Inspiration

- [Marginalia Search](https://search.marginalia.nu) - Non-commercial web index
- [Wiby.me](https://wiby.me) - Old web search engine
- [The Forest](https://theforest.link) - Curated link discovery
- [Gossip's Web](https://gossipsweb.net) - Handmade web directory

---

## Open Questions

1. **Authentication**: Should we support Are.na OAuth for users to add blocks to their own channels?

2. **Persistence**: Should exploration history be server-side (accounts) or client-only (localStorage)?

3. **Mobile**: Current iframe approach is desktop-centric. How to handle mobile better?

4. **Rate Limits**: How aggressively can we call Are.na API? Need to implement caching.

5. **Content Moderation**: Are.na is generally high-quality, but should we have any filtering?

---

*Document created: December 2024*
*For: Moonjump Explorer Enhancement*
