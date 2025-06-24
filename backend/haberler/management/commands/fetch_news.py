import feedparser
from django.core.management.base import BaseCommand
from haberler.models import Bulletin
from datetime import datetime
import time

FEEDS = [
    "https://thehackernews.com/feeds/posts/default",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://threatpost.com/feed/",
]

class Command(BaseCommand):
    help = 'Siber güvenlik haberlerini RSS kaynaklarından çeker'

    def handle(self, *args, **kwargs):
        for feed_url in FEEDS:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title
                content = entry.summary if hasattr(entry, 'summary') else ''
                link = entry.link
                published = (
                    datetime.fromtimestamp(time.mktime(entry.published_parsed))
                    if hasattr(entry, 'published_parsed')
                    else datetime.now()
                )

                if not Bulletin.objects.filter(title=title).exists():
                    Bulletin.objects.create(
                        title=title,
                        content=content + f"\n\nKaynak: {link}",
                        published_at=published
                    )
                    self.stdout.write(self.style.SUCCESS(f"✓ Eklendi: {title}"))
                else:
                    self.stdout.write(f"- Zaten var: {title}")
