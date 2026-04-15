import httpx
from rss_parser import RSSParser
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
            rss = RSSParser.parse(response.text)
            result = []

            for item in rss.channel.items[:10]:

                title = str(item.title)

                if hasattr(item, 'links') and item.links:
                    link = str(item.links[0])
                elif hasattr(item, 'link'):
                    link = str(item.link)
                else:
                    print("Fox Business: ссылка на загаловок не найдена")
                    continue

                if title and link and title != 'None':
                    result.append({
                        "title": title,
                        "url": link,
                        "source": self.source_name
                    })
            
            print(f"Fox Business: parsed {len(result)} news")
            return result
            
        except Exception as e:
            print(f"Fox Business parsing error: {e}")
            return []