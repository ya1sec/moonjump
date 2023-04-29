GET https://api.marginalia.nu/suggest/?partial={query}

Moonjump is a server that redirects you to a random page harvested from Are.na, Hacker News, Marginalia Search, and Gossip Web.

This project aims to spark curiosity and provide a portal to the vast collection of interesting material hidden by the commercial web.

The source material is aggregated with care by users of these platforms. Since this accumulation is performed by hand, pages are saved because they had an effect on the users who saved them. The goal is to find something that has an effect on you.

For Are.na, the dictionary of channels that the app pulls from is weighted by the number of pages in the channel. Channels with the most pages are more likely to be selected.

This collection of curious content is a trove of handcrafted treasures. But as our habits have taught us in the contemporary era of web surfing, we are prone to doomscrolling (and even doom-bookmarking).

Moonjump makes a decision for you by selecting something random from a deep sea of unconventional content. Results may be peculiar, profound, or absolute nonsense. But you can always close the tab and jump again.

The search engine is powered by Marginalia, an amazing project which indexes non-commercial content and may surprise you with sites you perhaps weren't aware of. I have to admit that the existance of Marginalia is a huge inspiration for Moonjump. Search queries on Moonjump use the Marginalia API to redirect you to a random result.

The easiest way to jump is to click the large logo at the center of the homepage. You can also add https://moonjump.app/jump to your bookmarks bar.

If you are an OSX user and have hammerspoon installed, check the github repo for instructions on how to jump via a keyboard shortcut. (This is really fun! I have mine mappt to Cmd-Ctrl-J)

If anyone has any suggestions for improvements, please let me know! Also feel free to open a pull request. The codebase for the homepage is a little bit of a mess but the main functionality is in the Flask app.



Links:

https://moonjump.app
https://moonjump.app/jump
https://moonjump.app/hn
https://github.com/ya1sec/moonjump

--

https://www.are.na
https://search.marginalia.nu
https://gossipsweb.net
