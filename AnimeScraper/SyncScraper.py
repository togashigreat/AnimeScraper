"""
This is the Synchronus version of `KunYu()` class.

This module contains the **SyncKunYu()** class, which acts as the primary entry point
for interacting with `Myanimelist <https://myanimelist.net/>`__ data, as well as helper classes and functions.
"""

from typing import Optional, List
import httpx
from ._model import Anime, Character
from .sync_malscraper import SyncMalScraper

class SyncKunYu:
    """
    The main class for interacting with MyAnimeList data.

    """

    def __init__(self) -> None:
        self.shared_client: Optional[httpx.Client] = None
    

    def __enter__(self):
        self.shared_client = httpx.Client(headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"

        })
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.shared_client:
            self.shared_client.close()

    def search_anime(self, anime_name: str)-> Anime:
        """
        Fetches and Returns Anime details from myanimelist.

        Args:
            anime_name (str): Name of the anime you want to search.
        
        Returns:
            Anime: Returns Anime object with anime details.

        Example:
            >>> from AnimeScraper import SyncKunYu
            >>> scraper = SyncKunYu()
            >>> anime = scraper.search_anime("dr stone")
            >>> print(anime.title)

        """

        with SyncMalScraper(client=self.shared_client) as scraper:
            anime = scraper.search_anime(anime_name)
            return anime


    def search_character(self, character_name: str)-> Character:
        """
        Fetches and Returns Character details from myanimelist.

        Args:
            character_name (str): Name of the Character you want to search.
        
        Returns:
            Character: Returns Character object with the character details.

        Example:
            >>> from AnimeScraper import SyncKunYu
            >>> with SyncKunYu() as scraper:
            >>>     character = scraper.search_character("Togashi Yuuta")
            >>>     print(character.name)

        Notes:
            - You can use `with` context manager for same session use.
        """
        with SyncMalScraper(client=self.shared_client) as scraper:
            character = scraper.search_character(character_name)
            return character 


    def get_anime(self, anime_id: str)->Anime:
        """
        Fetches anime details from MyAnimeList.

        Args:
            anime_id (str): The ID of the anime.

        Returns:
            Anime: An object containing anime details.
        """
        with SyncMalScraper(client=self.shared_client) as scraper:
            anime = scraper.get_anime(anime_id)
            return anime

    def get_character(self, character_id: str)-> Character:
        """
        Fetches character details from MyAnimeList.

        Args:
            character_id (str): The ID of the character.

        Returns:
            Character: An object containing character details.
        """
        with SyncMalScraper(client=self.shared_client) as scraper:
            character = scraper.get_character(character_id)
            return character

    def search_batch_anime(self, anime_names: List[str])-> List[Anime]:
        """
        Fetches anime details in batch.
        Args:
            anime_names (List(str)): List of anime names.

        Returns:
            List[Anime]: A list of Anime objects with Anime details.
        """

        with SyncMalScraper(client=self.shared_client) as scraper:
            anime_list = scraper.search_batch_anime(anime_names)

        return anime_list
    


    def search_batch_character(self, character_names: List[str])-> List[Character]:
        """
        Fetches character details in batch.
        Args:
            character_names (List(str)): List of characters name.

        Returns:
            List[Character]: A list of Character objects with character's details.
        """

        with SyncMalScraper(client=self.shared_client) as scraper:
            batch_characters = scraper.search_batch_character(character_names)

        return batch_characters
