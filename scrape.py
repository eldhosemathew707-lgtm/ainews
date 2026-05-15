import feedparser
from datetime import datetime

# Curated feeds for Agents, Local LLMs, and Open Source
FEEDS = [
    "https://rss.arxiv.org/rss/cs.AI",
    "https://huggingface.co/blog/feed.xml",
    "https://ollama.com/blog/rss",
    "https://lilianweng.github.io/posts/index.xml",
    "https://simonwillison.net/atom/entries/",
    "https://www.reddit.com/r/LocalLLaMA/.rss",
    "https://github.com/joaomdmoura/crewAI/releases.atom"
]

def generate_site():
    articles = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'source': feed.feed.get('title', 'Unknown Source'),
                    'date': entry.get('published', 'Recently')
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # Simple HTML Template with Water.css for a clean look
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI & Agentic News Radar</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
        <meta charset="utf-8">
    </head>
    <body>
        <h1>AI News Hub</h1>
        <p><i>Automated updates on Local LLMs, Agents, and OSS.</i></p>
        <p><strong>Last Refresh:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</p>
        <hr>
        {''.join([f"<div style='margin-bottom: 20px;'><h3><a href='{a['link']}' target='_blank'>{a['title']}</a></h3><small><b>Source:</b> {a['source']} | <b>Date:</b> {a['date']}</small></div>" for a in articles])}
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_site()