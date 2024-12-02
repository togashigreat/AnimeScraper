import aiohttp
from typing import Optional
from ._parse_anime_data import _parse_anime_data, get_character

from ._model import (
    Anime,
    AnimeCharacter,
    AnimeStats,
    Character
)

class MalScraper:
    """
    A class for interacting with MyAnimeList's website.

    This class handles fetching HTML data for anime and characters.

    Attributes:
        BASE_URL (str): The base URL for MyAnimeList.
        session (Optional[aiohttp.ClientSession]): The session used for HTTP requests.
    """
    BASE_URL = "https://myanimelist.net"

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        """
        Initializes the scraper with an optional aiohttp session.

        Args:
            session (Optional[aiohttp.ClientSession]): An existing HTTP session. If None, a new session will be created.
        """
        self.session = session
        self.own_session = session is None # True if this instance manages its own session

    async def __aenter__(self):
        """
        Enter the context manager.

        Returns:
            MalScraper: The current instance with an initialized session.
        """
        if not self.session:
            self.session = aiohttp.ClientSession(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

        })
        return self



    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager and close the session if owned.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Traceback.
        """
        if self.session and self.own_session:
            await self.session.close()


    async def _fetch_anime(self, anime_id: int)->str:
        """
        Fetch the HTML for a specific anime.

        Args:
            anime_id (int): The MyAnimeList ID of the anime.

        Returns:
            str: The HTML content of the anime page.

        Raises:
            RuntimeError: If the session is not initialized.
            ValueError: If the anime ID is not found.
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context. ")
        url = f"{self.BASE_URL}/anime/{anime_id}"
        async with self.session.get(url) as response: 
            if response.status == 404:
                raise ValueError(f"Anime with ID {anime_id} not found")
            html = await response.text()
        return html


    async def _fetch_character(self, character_id: int)->str:
        """
        Fetch the HTML for a specific character.

        Args:
            character_id (int): The MyAnimeList ID of the character.

        Returns:
            str: The HTML content of the character page.

        Raises:
            RuntimeError: If the session is not initialized.
            ValueError: If the character ID is not found.
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context. ")
        url = f"{self.BASE_URL}/character/{character_id}"
        async with self.session.get(url) as response:
            if response.status == 404:
                raise ValueError(f"Character with ID: {character_id} not found")
            html = await response.text()
        return html



    async def get_anime(self, anime_id: int)->Anime:
        """
        Fetch and parse anime details.

        Args:
            anime_id (int): The MyAnimeList ID of the anime.

        Returns:
            Anime: An object containing detailed anime information.
        """
        html = await self._fetch_anime(anime_id)
        parsed_anime_data = await _parse_anime_data(html)
        return await self.parse_anime(parsed_anime_data)


    async def get_character(self, character_id: int)-> Character:
        """
        Fetch and parse character details.

        Args:
            character_id (int): The MyAnimeList ID of the character.

        Returns:
            Character: An object containing detailed character information.
        """
        html = await self._fetch_character(character_id)
        character_details = await get_character(html)
        return Character(*character_details)


    async def parse_anime(self, parsed_anime_data: dict)-> Anime:
        """
        Convert parsed data into an Anime object.

        Args:
            parsed_anime_data (dict): Parsed data of the anime.

        Returns:
            Anime: An object containing detailed anime information.
        """
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

