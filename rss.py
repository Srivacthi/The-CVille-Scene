import feedparser

# URL of the RSS feed
rss_url = "https://www.cvilletomorrow.org/feed/"  # Replace with the actual RSS feed URL

# Parse the RSS feed
feed = feedparser.parse(rss_url)

print(f"Feed Title: {feed.feed.get('title', 'No Title Found')}")
print(f"Number of Entries: {len(feed.entries)}")

if not feed.entries:
    print("No entries found. The RSS feed might be empty or inaccessible.")
else:
    for entry in feed.entries[:5]:  # Print the first 5 entries
        print(f"Title: {entry.get('title', 'No Title')}")
        print(f"Link: {entry.get('link', 'No Link')}")
        print("-" * 50)