# app/parsers/reuters.py
import httpx
from rss_parser import RSSParser
from app.parsers.base import BaseParser


class ReutersParser(BaseParser):

    source_name = "reuters"
    base_url = "https://www.reuters.com"

    async def fetch_news(self):
        # Альтернативные RSS-фиды Reuters (рабочие)
        rss_urls = [
            "https://www.reutersagency.com/feed/?best-topics=news&post_type=best",
            "https://feeds.reuters.com/reuters/worldNews",
            "https://feeds.reuters.com/reuters/businessNews",
            "https://feeds.reuters.com/reuters/technologyNews",
        ]
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = None
            for rss_url in rss_urls:
                try:
                    response = await client.get(rss_url)
                    if response.status_code == 200:
                        print(f"Using Reuters feed: {rss_url}")
                        break
                except:
                    continue
            
            if not response or response.status_code != 200:
                print("All Reuters feeds unavailable")
                return []
        
        # Парсим RSS
        rss = RSSParser.parse(response.text)
        
        result = []
        for item in rss.channel.items[:10]:
            title = str(item.title)
            link = str(item.link)
            
            if title and link and not title.startswith('<!'):
                result.append({
                    "title": title,
                    "url": link,
                    "source": self.source_name
                })
        
        return result
