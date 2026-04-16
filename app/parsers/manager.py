import asyncio
from app.parsers.kommersant import KommersantParser
from app.parsers.rbk import RBKParser
from app.parsers.fox_business import FoxBusinessParser
from app.parsers.ria import RIAParser

PARSERS = [
    KommersantParser(),
    RBKParser(),
    FoxBusinessParser(),
    RIAParser(),
]


async def fetch_all_news():
    tasks = []
    for parser in PARSERS:
        tasks.append(fetch_parser_safely(parser))
    
    results = await asyncio.gather(*tasks)
    
    news = []
    for result in results:
        if result:
            news.extend(result)
    
    return news


async def fetch_parser_safely(parser):
    try:
        return await parser.fetch_news()
    except Exception as e:
        print(f"Parser {parser.source_name} failed: {e}")
        return []