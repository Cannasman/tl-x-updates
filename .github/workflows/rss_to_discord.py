import feedparser
import requests
import os

FEED_URL = "https://rsshub.app/twitter/user/playtlgame"  # Use alternate if needed
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]
STATE_FILE = "last_post.txt"

def get_last_posted():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_posted(link):
    with open(STATE_FILE, "w") as f:
        f.write(link)

def post_to_discord(title, link):
    message = {
        "content": f"🐦 New TL X Post:\n**{title}**\n🔗 {link}"
    }
    requests.post(DISCORD_WEBHOOK, json=message)

feed = feedparser.parse(FEED_URL)
if feed.entries:
    latest = feed.entries[0]
    last = get_last_posted()
    if latest.link != last:
        post_to_discord(latest.title, latest.link)
        save_last_posted(latest.link)
