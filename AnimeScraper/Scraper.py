from typing import Optional
import aiohttp

from _parse_anime_data import _parse_anime_data, get_character
from _model import (
    Anime,
    AnimeCharacter,
    AnimeStats,
    Character
)

class MalScraper:
    BASE_URL = "https://myanimelist.net"

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        self.session = session
        self.own_session = session is None # True if this instance manages its own session

    async def __aenter__(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

        })
        return self



    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and self.own_session:
            await self.session.close()


    async def _fetch_anime(self, anime_id: int):
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context. ")
        url = f"{self.BASE_URL}/anime/{anime_id}"
        async with self.session.get(url) as response: 
            if response.status == 404:
                raise ValueError(f"Anime with ID {anime_id} not found")
            html = await response.text()
        return html


    async def _fetch_character(self, character_id: int):
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context. ")
        url = f"{self.BASE_URL}/character/{character_id}"
        async with self.session.get(url) as response:
            if response.status == 404:
                raise ValueError(f"Character with ID: {character_id} not found")
            html = await response.text()
        return html



    async def get_anime(self, anime_id: int)->Anime:
        html = await self._fetch_anime(anime_id)
        
        parsed_anime_data = await _parse_anime_data(html)

        return await self.parse_anime(parsed_anime_data)


    async def get_character(self, character_id: int):
        html = await self._fetch_character(character_id)
        character_details = await get_character(html)
        return Character(*character_details)


    async def parse_anime(self, parsed_anime_data: dict)-> Anime:
        return Anime(
            id=parsed_anime_data["id"],
            title=parsed_anime_data["title"],
            english_title=parsed_anime_data["english_title"],
            japanese_title=parsed_anime_data["japanese_title"],
            anime_type=parsed_anime_data["anime_type"],
            episodes=parsed_anime_data["episodes"],
            status=parsed_anime_data["status"],
            aired=parsed_anime_data["aired"],
            duration=parsed_anime_data["duration"],
            premiered=parsed_anime_data["premiered"],
            rating=parsed_anime_data["rating"],
            synopsis=parsed_anime_data["synopsis"],
            genres=parsed_anime_data["genres"],
            studios=parsed_anime_data["studios"],
            themes=parsed_anime_data["themes"],
            stats=AnimeStats(*parsed_anime_data["stats"]),
            characters=[AnimeCharacter(*character) for character in parsed_anime_data["characters"]]
        )

class KunYu:
    """
    This is the main class. It handles interaction with Myanimelist.

    Methods:
    - get_anime: Fetches anime details based on its ID 

    - get_character: Fetches character details based on its ID

    """
    def __init__(self) -> None:
        """Initialize the KunYu scraper."""
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
        Fatches an anime details from MAL website by its ID 

        Args:
            - anime_id (int): The MAL id of the anime

        Retuns:
            - Anime (object):  An Anime object with the anime details
        """

        async with MalScraper(session=self.shared_session) as scraper:
            anime = await scraper.get_anime(anime_id)
            return anime

    async def get_character(self, character_id: int)-> Character:
        """
        Fatches a Character details from MAL website by its ID

        Args:
            - character_id (int): The MAL id of the Character

        Retuns:
            - Character (object): An Character obeject with character details
        """
        async with MalScraper(session=self.shared_session) as scraper:
            character = await scraper.get_character(character_id)
            return character
    


