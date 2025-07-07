from django.core.management.base import BaseCommand
from haberler.models import Bulletin

from datetime import datetime
from cybernews.cybernews import CyberNews


class Command(BaseCommand):
    help = 'CyberNews ile tüm kategorilerden haberleri çeker ve Bulletin tablosuna kaydeder (görsel, yazar, tarih dahil)'

    def handle(self, *args, **kwargs):
        cn = CyberNews()

        categories = [
            "general", "dataBreach", "cyberAttack", "vulnerability", "malware",
            "security", "cloud", "tech", "iot", "bigData",
            "business", "mobility", "research", "corporate", "socialMedia"
        ]

        all_news = []

        for category in categories:
            try:
                news_list = cn.get_news(category)
                all_news.extend(news_list)
                self.stdout.write(self.style.SUCCESS(f"{category} kategorisinden {len(news_list)} haber çekildi."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"{category} kategorisinden haber çekilirken hata: {e}"))

        self.stdout.write(f"Toplam {len(all_news)} haber çekildi.")

        for item in all_news:
            title = item.get('title') or item.get('headline') or 'Başlıksız Haber'
            # Link için farklı olasılıkları kontrol ediyoruz
            link = (
                item.get('link') or 
                item.get('url') or 
                item.get('newsURL') or 
                item.get('news_url') or 
                item.get('article_url')
            )
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
