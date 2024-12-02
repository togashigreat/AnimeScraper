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
        self.shared_session = aiohttp.ClientSession(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.shared_session:
            await self.shared_session.close()


    async def get_anime(self, anime_id: int)->Anime:
        """
        Fetches anime details from MyAnimeList.

        Args:
            anime_id (int): The ID of the anime.

        Returns:
            Anime: An object containing anime details.
        """
        async with MalScraper(session=self.shared_session) as scraper:
            anime = await scraper.get_anime(anime_id)
            return anime

    async def get_character(self, character_id: int)-> Character:
        """
        Fetches character details from MyAnimeList.

        Args:
            character_id (int): The ID of the character.

        Returns:
            Character: An object containing character details.
        """
        async with MalScraper(session=self.shared_session) as scraper:
            character = await scraper.get_character(character_id)
            return character
    


