"""
Scraper: A module to fetch and parse data from MyAnimeList.

This module contains the **KunYu()** class, which acts as the primary entry point
for interacting with `Myanimelist <https://myanimelist.net/>`__ data, as well as helper classes and functions.
"""

from typing import List, Optional
import aiohttp
from ._model import Anime, Character
from .async_malscraper import MalScraper

class KunYu:
    """
    The main class for interacting with MyAnimeList data.

    This class acts as the entry point for users of the library.

    """



    def __init__(
            self, 
            use_cache: bool = False, 
            db_path: str = "cache.db",
            max_requests: int = 5,
            per_second: int = 1,
            timeout: int = 10
    ) -> None:
        """
        Initial method.

        Args:
            use_cache (bool): If data should be cached. (Default: False)
            db_path: (str): The path of the database. (Default: cache.db)
            max_requests (int): The number requests to make at `per_second` seconds. (Default: 5)
            per_second (int): number of seconds `max_requests` can be made. (Default: 1)

        """


        self.shared_session: Optional[aiohttp.ClientSession] = None
        self.Scraper = MalScraper(
            session=self.shared_session,
            use_cache=use_cache,
            db_path=db_path,
            max_requests=max_requests,
            per_second=per_second,
            timeout=timeout
        )
    




    async def __aenter__(self):
        # These Headers are needed in oder to get porper response from MAL
        self.shared_session = aiohttp.ClientSession(
            headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
            })

        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.shared_session:
            await self.shared_session.close()




    async def search_anime(self, anime_name: str)-> Anime:
        """
        Fetches and Returns Anime details from myanimelist.

        Args:
            anime_name (str): Name of the anime you want to search.
        
        Returns:
            Anime: Returns Anime object with anime details.
        """

        async with self.Scraper as scraper:
            anime = await scraper.search_anime(anime_name)
            return anime




    async def search_character(self, character_name: str)-> Character:
        """
        Fetches and Returns Character details from myanimelist.

        Args:
            character_name (str): Name of the Character you want to search.
        
        Returns:
            Character: Returns Character object with the character details.
        """

        async with self.Scraper as scraper:
            character = await scraper.search_character(character_name)
            return character



    async def get_anime(self, anime_id: str)->Anime:
        """
        Fetches anime details from MyAnimeList.

        Args:
            anime_id (str): The ID of the anime.

        Returns:
            Anime: An object containing anime details.
        """

        async with self.Scraper as scraper:
            anime = await scraper.get_anime(anime_id)
            return anime




    async def get_character(self, character_id: str)-> Character:
        """
        Fetches character details from MyAnimeList.

        Args:
            character_id (str): The ID of the character.

        Returns:
            Character: An object containing character details.
        """

        async with self.Scraper as scraper:
            character = await scraper.get_character(character_id)
            return character


    async def search_batch_anime(self, anime_names: List)-> List[Anime]:
        """
        Fetches multiple anime in batch.

        Args:
            anime_names (List): List of anime names.

        Returns:
            List[Anime]: Returns a list of Anime class object with anime details.

        """

        async with self.Scraper as scraper:
            batch_anime = await scraper.search_batch_anime(anime_names)
            return batch_anime 



    async def search_batch_character(self, character_names: List)-> List[Character]:
        """
        Fetches multiple characters in batch.

        Args:
            character_names (List): List of characters name.

        Returns:
            List[Character]: Returns a list of Character class object with characters details.

        """

        async with self.Scraper as scraper:
            batch_characters = await scraper.search_batch_character(character_names)
            return batch_characters
        
