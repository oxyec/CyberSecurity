import feedparser
from datetime import datetime
from time import mktime
import re

class NewsFetcher:
    def __init__(self):
        self.sources = [
            {
                'name': 'The Hacker News',
                'url': 'https://feeds.feedburner.com/TheHackersNews',
                'image_fallback': 'https://thehackernews.com/images/logo-dark.png'
            },
            {
                'name': 'BleepingComputer',
                'url': 'https://www.bleepingcomputer.com/feed/',
                'image_fallback': None
            },
            {
                'name': 'Wired Security',
                'url': 'https://www.wired.com/feed/category/security/latest/rss',
                'image_fallback': None
            },
             {
                'name': 'Turk Internet',
                'url': 'https://turk-internet.com/feed/',
                'image_fallback': None
            }
        ]

    def _extract_image(self, entry):
        # 1. Try 'media_content' (standard RSS media extension)
        if 'media_content' in entry:
            media = entry['media_content']
            if isinstance(media, list) and len(media) > 0:
                return media[0].get('url')

        # 2. Try 'media_thumbnail'
        if 'media_thumbnail' in entry:
            thumbs = entry['media_thumbnail']
            if isinstance(thumbs, list) and len(thumbs) > 0:
                return thumbs[0].get('url')

        # 3. Try finding <img> tag in description/summary
        content = entry.get('summary', '') or entry.get('description', '')
        match = re.search(r'<img[^>]+src="([^">]+)"', content)
        if match:
            return match.group(1)

        return None

    def _clean_content(self, html_content):
        # Remove HTML tags for clean text, or keep basic formatting
        # For now, let's just strip image tags to avoid duplicates if we show image separately
        clean = re.sub(r'<img[^>]*>', '', html_content)
        # remove empty paragraphs
        clean = re.sub(r'<p>\s*</p>', '', clean)
        return clean.strip()

    def fetch_all(self):
        all_news = []
        for source in self.sources:
            try:
                print(f"Fetching from {source['name']}...")
                feed = feedparser.parse(source['url'])

                for entry in feed.entries:
                    # Parse date
                    published_at = datetime.now()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                         published_at = datetime.fromtimestamp(mktime(entry.published_parsed))
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                         published_at = datetime.fromtimestamp(mktime(entry.updated_parsed))

                    image_url = self._extract_image(entry) or source['image_fallback']

                    # Content prioritization
                    content = entry.get('summary', '') or entry.get('description', '')

                    item = {
                        'title': entry.title,
                        'link': entry.link,
                        'content': self._clean_content(content),
                        'published_at': published_at,
                        'image_url': image_url,
                        'author': source['name']  # Use source as author if specific author not found
                    }
                    all_news.append(item)

            except Exception as e:
                print(f"Error fetching from {source['name']}: {e}")

        # Sort by date descending
        all_news.sort(key=lambda x: x['published_at'], reverse=True)
        return all_news
