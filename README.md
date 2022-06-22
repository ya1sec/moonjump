<!-- <h1 align="center">Moonjump</h1> -->

<img width="90px" src="https://raw.githubusercontent.com/ya1sec/moonjump/508770b57683b0012789dbd01fa31f8a19eeb8d9/static/assets/img/jupiter-purple.svg" alt="moonjump">
<p align="center">
</p>

# Moonjump

Moonjump is a server that redirects you to a random page harvested from [are.na](https://are.na) or [Hacker News](https://news.ycombinator.com).

## Usage

Try it out: [moonjump.app](https://moonjump.com)

There are a few ways to make shortcuts to moonjump

1. Add https://moonjump.app to your bookmarks bar and use it to jump to a random page.
2. If you have OSX and Hammerspoon installed, you can map a shortcut to open moonjump in your default browser.
   - I have mine mapped to `Cmd+Ctrl+J`

```lua
hs.hotkey.bind({"cmd", "ctrl"}, "j", function()
	hs.execute("open 'https://moonjump.app'")
end)
```

3. To launch from your shell, add the following to your `~/.zshrc` or `~/.bashrc` file:

```bash
alias moonjump='open "https://moonjump.app"'
```

- [moonjump.app](https://moonjump.app) serves from the are.na list
- [moonjump.app/hn](https://moonjump.app/hn) serves from the Hacker News list

### Are.na

A dictionary of the channels that are currently being used can be found at the top of `lib/arena.py`

Note that since the are.na api is paginated, the dictionary of channels is weighted by the number of pages in the channel. Channels with the most pages are more likely to be selected.

### Hacker News

Get served a random link from Top Stories, Best Stories, or New Stories. Additional parameters and configuration might be added in the future.

## Contributing

If you want to contribute, DM me or open a pull request. Things may be added or changed as needed.

## TODO

- Bookmarklet
- Extension
- Hammerspoon Spoon
- Customization
- lynx (text only sites)
