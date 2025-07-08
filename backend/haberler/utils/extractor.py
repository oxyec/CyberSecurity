import httpx
from bs4 import BeautifulSoup


class Extractor:
    def __init__(self):
        self.client = httpx.Client(timeout=10.0)

    def data_extractor(self, sources):
        """
        sources: list of dict, örn:
        [
            {
                "https://example.com/news": {
                    "headlines": "css selector",
                    "author": "css selector",
                    "fullNews": "css selector",  # detay sayfa için geçerli
                    "newsImg": "css selector",
                    "newsURL": "css selector",
                    "date": "css selector"
                }
            },
            ...
        ]
        """
        all_news = []

        for source in sources:
            for url, selectors in source.items():
                try:
                    response = self.client.get(url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "lxml")

                    headlines = soup.select(selectors.get("headlines", ""))
                    authors = soup.select(selectors.get("author", "")) if selectors.get("author") else []
                    news_imgs = soup.select(selectors.get("newsImg", "")) if selectors.get("newsImg") else []
                    news_urls = soup.select(selectors.get("newsURL", "")) if selectors.get("newsURL") else []
                    dates = soup.select(selectors.get("date", "")) if selectors.get("date") else []

                    # Haber sayısı başlık sayısına göre
                    count = len(headlines)

                    # Haber linklerini al (detay sayfa URL'leri)
                    urls = []
                    for a in news_urls:
                        if a.has_attr("href"):
                            href = a["href"]
                            # Eğer URL tam değilse tam URL yap (ör: relative link)
                            if href.startswith("/"):
                                from urllib.parse import urljoin
                                href = urljoin(url, href)
                            urls.append(href)

                    for i in range(count):
                        news_item = {}

                        news_item["headline"] = headlines[i].get_text(strip=True) if i < len(headlines) else None
                        news_item["author"] = authors[i].get_text(strip=True) if i < len(authors) else None
                        news_item["newsImg"] = news_imgs[i]["src"] if i < len(news_imgs) and news_imgs[i].has_attr("src") else None
                        news_item["newsURL"] = urls[i] if i < len(urls) else None
                        news_item["date"] = dates[i].get_text(strip=True) if i < len(dates) else None

                        # Detay sayfaya gidip tam haber metnini çek
                        full_news_text = None
                        detail_url = news_item["newsURL"]
                        if detail_url and selectors.get("fullNews"):
                            try:
                                detail_response = self.client.get(detail_url)
                                detail_response.raise_for_status()
                                detail_soup = BeautifulSoup(detail_response.text, "lxml")
                                full_news_elem = detail_soup.select_one(selectors["fullNews"])
                                if full_news_elem:
                                    full_news_text = full_news_elem.get_text(strip=True)
                            except Exception as e:
                                print(f"Error fetching detail page {detail_url}: {e}")

                        news_item["fullNews"] = full_news_text

                        all_news.append(news_item)

                except Exception as e:
                    print(f"Error fetching {url}: {e}")

        return all_news
