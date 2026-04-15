from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    async def fetch_news(self):
        pass