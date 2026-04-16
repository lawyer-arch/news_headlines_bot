import httpx
import feedparser
from datetime import datetime
from app.parsers.base import BaseParser


class FoxBusinessParser(BaseParser):

    source_name = "fox_business"
    base_url = "https://www.foxbusiness.com"

    async def fetch_news(self):
        rss_url = "https://moxie.foxbusiness.com/google-publisher/latest.xml"
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            try:
                response = await client.get(rss_url)
                if response.status_code != 200:
                    print(f"Fox Business ответил {response.status_code}")
                    return []
            except Exception as e:
                print(f"Fox Business error: {e}")
                return []

        try:
            feed = feedparser.parse(response.text)
            result = []

            for entry in feed.entries[:10]:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                
                # Извлекаем дату публикации
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'published'):
                    # Пробуем распарсить строку с датой
                    try:
                        from dateutil import parser
                        published = parser.parse(entry.published)
                    except:
                        pass
                
                if title and link:
                    result.append({
                        "title": title,
                        "url": link,
                        "source": self.source_name,
                        "published_at": published  # Добавляем дату
                    })
            
            print(f"Fox Business: parsed {len(result)} news")
            return result
            
        except Exception as e:
            print(f"Fox Business parsing error: {e}")
            return []