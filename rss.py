import feedparser

feed_url = "https://www.charlottesville.gov/RSSFeed.aspx?ModID=58&CID=Events-Programs-22"
feed = feedparser.parse(feed_url)

for entry in feed.entries:
    print(f"Event: {entry.title}")
    print(f"Date: {entry.published}")
    print(f"Description: {entry.summary}\n")