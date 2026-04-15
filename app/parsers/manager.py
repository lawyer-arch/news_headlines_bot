import asyncio

from app.parsers.kommersant import KommersantParser
from app.parsers.rbk import RBKParser
#from app.parsers.bloomberg import BloombergParser
from app.parsers.fox_business import FoxBusinessParser
from app.parsers.ria import RIAParser

PARSERS = [
    KommersantParser(),
    RBKParser(),
    FoxBusinessParser(),
    RIAParser(),
    # BloombergParser(),
]


async def fetch_all_news():

    tasks = [parser.fetch_news() for parser in PARSERS]

    results = await asyncio.gather(*tasks)

    news = []

    for result in results:
        news.extend(result)

    return news
