from django.core.management.base import BaseCommand
from haberler.models import Bulletin
from haberler.utils.news_fetcher import NewsFetcher
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fetches cybersecurity news from RSS feeds and saves to Bulletin model'

    def handle(self, *args, **kwargs):
        fetcher = NewsFetcher()
        news_items = fetcher.fetch_all()

        self.stdout.write(f"Fetched {len(news_items)} items total. Processing...")

        added_count = 0
        for item in news_items:
            # Check if exists (by link)
            if not Bulletin.objects.filter(link=item['link']).exists():
                try:
                    # Make aware if naive
                    pub_date = item['published_at']
                    if timezone.is_naive(pub_date):
                        pub_date = timezone.make_aware(pub_date)

                    Bulletin.objects.create(
                        title=item['title'],
                        content=item['content'],
                        link=item['link'],
                        published_at=pub_date,
                        image_url=item['image_url'],
                        author=item['author']
                    )
                    added_count += 1
                    self.stdout.write(self.style.SUCCESS(f"+ Added: {item['title']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error saving {item['title']}: {e}"))
            else:
                # self.stdout.write(f". Skipped (exists): {item['title']}")
                pass

        self.stdout.write(self.style.SUCCESS(f"Successfully added {added_count} new bulletins."))
