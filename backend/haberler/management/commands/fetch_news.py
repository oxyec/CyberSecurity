from django.core.management.base import BaseCommand
from haberler.models import Bulletin
from haberler.cybernews import CyberNews
from datetime import datetime

class Command(BaseCommand):
    help = 'CyberNews ile tüm haberleri çeker ve Bulletin tablosuna kaydeder (görsel, yazar, tarih dahil)'

    def handle(self, *args, **kwargs):
        cn = CyberNews()

        try:
            all_news = cn.get_news()
            self.stdout.write(f"{len(all_news)} haber çekildi.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Haber çekilirken hata: {e}"))
            return

        for item in all_news:
            title = item.get('title') or item.get('headline')
            link = item.get('link') or item.get('url')
            content = item.get('summary') or item.get('full_text') or ''
            image_url = item.get('image') or item.get('image_url') or ''
            author = item.get('author') or ''
            
            published_str = item.get('date') or item.get('published_at') or None
            if published_str:
                try:
                    published = datetime.fromisoformat(published_str)
                except Exception:
                    published = datetime.now()
            else:
                published = datetime.now()

            if link and not Bulletin.objects.filter(link=link).exists():
                Bulletin.objects.create(
                    title=title,
                    content=content + f"\n\nKaynak: {link}",
                    link=link,
                    published_at=published,
                    image_url=image_url,
                    author=author
                )
                self.stdout.write(self.style.SUCCESS(f"✓ Eklendi: {title}"))
            else:
                self.stdout.write(f"- Zaten var veya link yok: {title}")
