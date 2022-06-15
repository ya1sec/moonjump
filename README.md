<!-- <h1 align="center">Moonjump</h1> -->

<img width="90px" src="./assets/moonjump.png" alt="moonjump">
<p align="center">
</p>

# Moonjump

Moonjump redirects you to a random interesting page out of thousands curated on [are.na](https://are.na) or [Hacker News](https://news.ycombinator.com).

## Usage

### Are.na

Are.na channels are weighted by the length of their contents. Channels with more content are more likely to be selected.

A dictionary of the channels that are currently being used can be found at the top of `lib/arena.py`

Note that since the are.na api is paginated, the dictionary of channels is weighted by the number of pages in the channel, so that the channels with the most pages are more likely to be selected.

### Hacker News

HN is in the works...

## Contributing

If you want to contribute, please DM me or open a pull request. Things may be added or changed as needed.

## TODO

- Bookmarklet
- Extension
- Hammerspoon Spoon
- Easy config
