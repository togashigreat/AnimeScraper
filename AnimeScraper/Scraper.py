"""
Scraper: A module to fetch and parse data from MyAnimeList.

This module contains the **KunYu()** class, which acts as the primary entry point
for interacting with `Myanimelist <https://myanimelist.net/>`__ data, as well as helper classes and functions.
"""

from typing import Optional
import aiohttp

from ._model import Anime, Character
from .malscraper import MalScraper

class KunYu:
    """
    The main class for interacting with MyAnimeList data.

    This class acts as the entry point for users of the library.

    """

    def __init__(self) -> None:
        self.shared_session: Optional[aiohttp.ClientSession] = None
    

    async def __aenter__(self):
        self.shared_session = aiohttp.ClientSession(headers = {
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
        async with MalScraper(session=self.shared_session) as scraper:
            anime = await scraper.search_anime(anime_name)
            return anime

    async def get_anime(self, anime_id: str)->Anime:
        """
        Fetches anime details from MyAnimeList.

        Args:
            anime_id (str): The ID of the anime.

        Returns:
            Anime: An object containing anime details.
        """
        async with MalScraper(session=self.shared_session) as scraper:
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
        async with MalScraper(session=self.shared_session) as scraper:
            character = await scraper.get_character(character_id)
            return character
    


