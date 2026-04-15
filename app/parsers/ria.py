# app/parsers/ria.py
from app.parsers.base import BaseParser
import httpx
import feedparser


class RIAParser(BaseParser):
    
    source_name = "ria"
    base_url = "https://ria.ru"

    async def fetch_news(self):
        rss_url = "https://ria.ru/export/rss2/archive/index.xml"
        
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=30.0
        ) as client:
            try:
                response = await client.get(rss_url)
                if response.status_code != 200:
                    return []
            except Exception as e:
                print(f"РИА ошибка: {e}")
                return []
        
        # Используем feedparser для парсинга RSS
        feed = feedparser.parse(response.text)
        
        result = []
        for entry in feed.entries[:10]:
            title = entry.get('title', '')
            link = entry.get('link', '')
            
            if title and link:
                result.append({
                    "title": title,
                    "url": link,
                    "source": self.source_name
                })
        
        print(f"РИА Новости: получено {len(result)} новостей")
        return result
