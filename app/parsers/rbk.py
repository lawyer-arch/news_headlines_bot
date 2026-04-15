from app.parsers.base import BaseParser
import httpx
from bs4 import BeautifulSoup


class RBKParser(BaseParser):
    
    source_name = "rbk"
    base_url = "https://www.rbc.ru"

    async def fetch_news(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        async with httpx.AsyncClient(
            headers=headers,
            follow_redirects=True,
            timeout=30.0
        ) as client:
            try:
                response = await client.get("https://www.rbc.ru/")
                if response.status_code != 200:
                    return []
            except Exception as e:
                print(f"РБК ошибка: {e}")
                return []

        soup = BeautifulSoup(response.text, "html.parser")
        news = []

        # Ищем все ссылки на новости по структуре из HTML
        # Берём .news-line-wrapper, внутри него .news-line-title и родительскую ссылку
        news_wrappers = soup.select(".news-line-wrapper")
        
        for wrapper in news_wrappers[:15]:
            # Ищем ссылку внутри wrapper
            link = wrapper.find('a')
            if not link:
                continue
            
            href = link.get('href')
            if not href:
                continue
            
            # Ищем заголовок внутри .news-line-title
            title_elem = wrapper.select_one(".news-line-title")
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                title = link.get_text(strip=True)
            
            if not title or len(title) < 10:
                continue
            
            # Формируем полный URL
            if href.startswith('/'):
                full_url = "https://www.rbc.ru" + href
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = "https://www.rbc.ru/" + href
            
            news.append({
                "title": title,
                "url": full_url,
                "source": self.source_name
            })
        
        # Удаляем дубликаты
        unique_news = []
        seen_urls = set()
        for item in news:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_news.append(item)
        
        print(f"РБК: получено {len(unique_news)} новостей")
        return unique_news[:10]
