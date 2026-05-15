import feedparser
from datetime import datetime
import os

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
    print("Starting scrape...")
    
    for url in FEEDS:
        # Adding an agent helps prevent getting blocked by RSS providers
        feed = feedparser.parse(url, agent='Mozilla/5.0 (AI News Bot)')
        
        if not feed.entries:
            print(f"Warning: No entries found for {url}")
            continue
            
        for entry in feed.entries[:5]:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'source': feed.feed.get('title', 'AI Source'),
                'date': entry.get('published', 'Recent')
            })

    # If no articles were found at all, don't overwrite with a blank page
    if not articles:
        print("Error: No articles found across all feeds.")
        return

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI & Agentic Hub</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
        <style>
            body {{ max-width: 900px; margin: auto; padding: 20px; }}
            .card {{ border-bottom: 1px solid #444; padding: 15px 0; }}
            .source {{ color: #007bff; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>🚀 AI & Open Source News</h1>
        <p><strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</p>
        <hr>
        {''.join([f"<div class='card'><h3><a href='{a['link']}' target='_blank'>{a['title']}</a></h3><p><span class='source'>{a['source']}</span> | <small>{a['date']}</small></p></div>" for a in articles])}
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Successfully generated index.html")

if __name__ == "__main__":
    generate_site()
