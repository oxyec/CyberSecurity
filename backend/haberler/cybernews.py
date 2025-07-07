import requests
from bs4 import BeautifulSoup

class CyberNews:
    """
    Basit cyber security haberlerini çeken sınıf.
    Şu an The Hacker News'tan son haber başlık ve linklerini çeker.
    """

    def __init__(self):
        self.source_url = "https://thehackernews.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def get_news(self):
        try:
            response = requests.get(self.source_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Haber çekilirken hata oluştu: {e}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="body-post")

        news_list = []
        for article in articles:
            title_tag = article.find("h2", class_="home-title")
            link_tag = article.find("a", class_="story-link")
            summary_tag = article.find("div", class_="home-desc")

            title = title_tag.text.strip() if title_tag else "Başlıksız"
            link = link_tag["href"] if link_tag else ""
            summary = summary_tag.text.strip() if summary_tag else ""

            news_list.append({
                "title": title,
                "link": link,
                "summary": summary
            })

        return news_list
