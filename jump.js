function weightedRandom(min, max) {
  return Math.round(max / (Math.random() * max + min));
}

/*
internet-escape
thirsty-for-knowledge
site-cite-sight
internet-surfing-clubs
we-should-talk-about-this-website
www-62v_kltr0d8
*/

let channels = [
  `bookmarks-1ntdk32bur0?page=${Math.floor(Math.random() * 6) + 1}`,
  `internet-escape?page=${Math.floor(Math.random() * 11) + 1}`,
  "thirsty-for-knowledge",
  "site-cite-sight",
  "internet-surfing-clubs",
  "we-should-talk-about-this-website",
  "www-62v_kltr0d8",
  "links-to-the-cultural-revolution",
];

class Arena {
  constructor() {
    let weighted_index = weightedRandom(1, channels.length) - 1;
    console.log(weighted_index);
    this.channel = channels[weighted_index];
  }

  requestChannel() {
    let channel = this.channel;
    console.log(channel);
    let url = `https://api.are.na/v2/channels/${channel}?per=5000`;
    return fetch(url, { method: "GET", redirect: "follow" })
      .then((response) => response.json())
      .then((data) => {
        return data;
      })
      .catch((error) => console.log("error", error));
  }

  async processContent() {
    let data = await this.requestChannel();
    console.log(data);
    if (data.contents.length == 0) {
      console.log("no contents");
      get_channel_contents_loop();
    } else {
      console.log(data.contents.length);
      let contents = data.contents;
      let random_item = contents[Math.floor(Math.random() * contents.length)];

      try {
        if ("source" in random_item) {
          let source = random_item.source;
          if ("url" in source) {
            let source_url = source.url;
            console.log(source_url);
            // NOTE: Redirect to source_url
            window.location.href = source_url;
          } else {
            window.location.reload();
          }
        } else {
          window.location.reload();
        }
      } catch (error) {
        console.log(error);
        window.location.reload();
      }
    }
  }
}

let a = new Arena();
a.processContent();
