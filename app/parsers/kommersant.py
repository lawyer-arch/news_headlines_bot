from app.parsers.base import BaseParser
import httpx
from bs4 import BeautifulSoup


class KommersantParser(BaseParser):
    
    source_name = "kommersant"
    base_url = "https://www.kommersant.ru"

    async def fetch_news(self):

        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_url)

        soup = BeautifulSoup(r.text, "html.parser")

        news = []

        for item in soup.select(".uho__link")[:10]:

            title = item.text.strip()
            link = self.base_url + item["href"]

            news.append({
                "title": title,
                "url": link,
                "source": self.source_name
            })

        return news
