import asyncio

from app.parsers.kommersant import KommersantParser
from app.parsers.reuters import ReutersParser
from app.parsers.bloomberg import BloombergParser

PARSERS = [
    KommersantParser(),
    ReutersParser(),
    BloombergParser(),
]


async def fetch_all_news():

    tasks = [parser.fetch_news() for parser in PARSERS]

    results = await asyncio.gather(*tasks)

    news = []

    for result in results:
        news.extend(result)

    return news
