import httpx
from bs4 import BeautifulSoup

from app.parsers.base import BaseParser


class ReutersParser(BaseParser):

    source_name = "reuters"
    base_url = "https://www.reuters.com"

    async def fetch_news(self):

        async with httpx.AsyncClient() as client:
            r = await client.get(self.base_url)

        soup = BeautifulSoup(r.text, "html.parser")

        news = []

        for item in soup.select("a[data-testid='Heading']")[:10]:

            title = item.text.strip()
            link = self.base_url + item["href"]

            news.append(
                {
                    "title": title,
                    "url": link,
                    "source": "reuters"
                }
            )

        return news
