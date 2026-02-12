import feedparser
from datetime import datetime
from time import mktime
import logging
import re

from django.conf import settings

logger = logging.getLogger(__name__)


class NewsFetcher:
    def __init__(self, sources=None):
        self.sources = sources or getattr(settings, 'NEWS_FEED_SOURCES', [])

    def _extract_image(self, entry):
        if 'media_content' in entry:
            media = entry['media_content']
            if isinstance(media, list) and len(media) > 0:
                return media[0].get('url')

        if 'media_thumbnail' in entry:
            thumbs = entry['media_thumbnail']
            if isinstance(thumbs, list) and len(thumbs) > 0:
                return thumbs[0].get('url')

        content = entry.get('summary', '') or entry.get('description', '')
        match = re.search(r'<img[^>]+src="([^">]+)"', content)
        if match:
            return match.group(1)

        return None

    def _clean_content(self, html_content):
        clean = re.sub(r'<img[^>]*>', '', html_content)
        clean = re.sub(r'<p>\s*</p>', '', clean)
        return clean.strip()

    def fetch_all(self):
        all_news = []
        for source in self.sources:
            try:
                logger.info("Fetching from %s...", source['name'])
                feed = feedparser.parse(source['url'])

                for entry in feed.entries:
                    published_at = datetime.now()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published_at = datetime.fromtimestamp(mktime(entry.published_parsed))
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published_at = datetime.fromtimestamp(mktime(entry.updated_parsed))

                    image_url = self._extract_image(entry) or source.get('image_fallback')

                    content = entry.get('summary', '') or entry.get('description', '')

                    item = {
                        'title': entry.title,
                        'link': entry.link,
                        'content': self._clean_content(content),
                        'published_at': published_at,
                        'image_url': image_url,
                        'author': source['name'],
                    }
                    all_news.append(item)

            except Exception as e:
                logger.error("Error fetching from %s: %s", source['name'], e)

        all_news.sort(key=lambda x: x['published_at'], reverse=True)
        return all_news
