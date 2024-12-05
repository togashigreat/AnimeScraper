import re
import aiohttp
from typing import Optional
from rapidfuzz import fuzz, process
from urllib.parse import quote

from ._parse_anime_data import _parse_anime_data, get_id, parse_anime_search, parse_character_search, parse_the_character

from ._model import (
    Anime,
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
            self.session = aiohttp.ClientSession(headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
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


    async def _fetch(self, url: str):
        """
        Fetch the HTML for a specific URL.

        Args:
            url (str): URL related to MyAnimeList.

        Returns:
            str: The HTML content of the anime page.

        Raises:
            RuntimeError: If the session is not initialized.
            ValueError: If the anime/character ID is not found.
        """

        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context. ")
        async with self.session.get(url) as response:
            if response.status == 404:
                raise ValueError(f"No data found with URL: {url}")
            html = await response.text()
            return html



    async def get_anime(self, anime_id: str)->Anime:
        """
        Fetch and parse anime details.

        Args:
            anime_id (str): The MyAnimeList ID of the anime.

        Returns:
            Anime: An object containing detailed anime information.
        """

        url = f"{self.BASE_URL}/anime/{anime_id}"

        html = await self._fetch(url)

        return await _parse_anime_data(html)



    async def get_character(self, character_id: str)-> Character:
        """
        Fetch and parse character details.

        Args:
            character_id (str): The MyAnimeList ID of the character.

        Returns:
            Character: An object containing detailed character information.
        """

        url = f"{self.BASE_URL}/character/{character_id}"

        html = await self._fetch(url)

        character_details = await parse_the_character(html)

        return character_details


    def normalize(self, text)-> str:
        return re.sub(r"[^a-zA-Z0-9\s]", "", text).lower()


    def get_close_match(self, query, lists):
        return process.extractOne(self.normalize(query), lists, scorer=fuzz.ratio)
    def save(self, html, path):
        with open(path, "w") as f:
            f.write(html)


    async def search_anime(self, query: str):
        """
        Search anime by name in myanimelist.net

        Args:
            query (str): The name of the anime.

        Returns:
            Anime: An Anime object with Anime Details.
        """
        url = f"{self.BASE_URL}/anime.php?q={quote(query)}&cat=anime"
        html = await self._fetch(url)
        start = '<table border="0" cellpadding="0" cellspacing="0" width="100%">'
        end = '<td class="borderClass bgColor1" valign="top" width="50">'

        # spliting and getting table contents remove useless codes
        anime_lists = "".join(html.split(start)[1].split(end, 9)[1:-1])
        # ((anime name, anime url)) tuple
        allanime = parse_anime_search(anime_lists)
        animeNames = tuple((x[0] for x in allanime))

        matched = self.get_close_match(query, animeNames)
        # if match rate > 50 return matched anime else first anime from list
        index = matched[2] if matched[1] > 50 else 0
        url = allanime[index][1]
        return await self.get_anime(get_id(url))



    async def search_character(self, query: str):
        """
        Search Character by name in myanimelist.net

        Args:
            query (str): The name of the Character.

        Returns:
            Character: A Character object with The Character Details.
        """

        url = f"{self.BASE_URL}/character.php?q={query}&cat=character"
        html = await self._fetch(url)
        start = '<table border="0" cellpadding="0" cellspacing="0" width="100%">'
        end = '</table>'

        # getting all the Character row from table of search results
        table = html.split(start)[1].split(end)[0].split('width="175">', 8)
        chars = tuple((parse_character_search(x) for x in table))

        names = tuple((self.normalize(x[0]) for x in chars))

        # if match rate higher than 50 return match else first char
        matched = self.get_close_match(query, names)
        index = matched[2] if matched[1] > 50 else 0
        
        url = chars[index][1]

        return await self.get_character(get_id(url))
