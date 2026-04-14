import httpx
from bs4 import BeautifulSoup


URL = "https://www.bloomberg.com"


async def fetch_news():

    async with httpx.AsyncClient() as client:
        r = await client.get(URL)

    soup = BeautifulSoup(r.text, "html.parser")

    result = []

    for item in soup.select(".uho__link")[:10]:

        title = item.text.strip()
        link = "https://www.bloomberg.com" + item["href"]

        result.append(
            {
                "title": title,
                "url": link
            }
        )

    return result