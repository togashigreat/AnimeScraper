import aiohttp, asyncio
from typing import Optional, List
from urllib.parse import quote
from aiolimiter import AsyncLimiter
from aiohttp import ClientTimeout
import aiosqlite
from .exceptions import (
    CharacterNotFoundError,
    AnimeNotFoundError,
    NetworkError
)
from ._cache_utils import _get_from_cache, _initialize_database, _store_in_cache

from ._parse_anime_data import (
    get_id,
    _parse_anime_data,  
    parse_anime_search, 
    parse_character_search, 
    parse_the_character,
    get_close_match,
    normalize
)

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
    ANIME = 10 # anime
    CHARACTER = 20 # character

    # needed for proper response from MAL
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

    def __init__(
        self, 
        use_cache: bool,
        db_path: str ,
        max_requests: int,
        per_second: int,
        timeout: int,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        """
        Initializes the scraper with an optional aiohttp session.

        Args:
            session (Optional[aiohttp.ClientSession]): An existing HTTP session. If None, a new session will be created.
        """
        self.session = session
        self.own_session = session is None # True if this instance manages its own session
        self.limiter = AsyncLimiter(max_requests, per_second)
        self.timeout = ClientTimeout(total=timeout)
        self.use_cache = use_cache
        self.db_path = db_path
        self.db: aiosqlite.Connection | None= None


    async def __aenter__(self):
        """
        Enter the context manager.

        Returns:
            MalScraper: The current instance with an initialized session.
        """
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.HEADERS)
        if self.use_cache:
            await _initialize_database(self.db_path)
            self.db = await aiosqlite.connect(self.db_path)
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
            self.session = None
        if self.db:
            await self.db.close()


    async def _fetch(self, url: str, req: int, query: str)-> str:
        """
        Fetch the HTML for a specific URL.

        Args:
            url (str): URL related to MyAnimeList.
            req (int): CHARACTER or ANIME
            query (str): The arguemnt passed to the get/search function (name, id etc.)

        Returns:
            str: The HTML content of the anime page.

        Raises:
            RuntimeError: If the session is not initialized.
            ValueError: If the anime/character ID is not found.
        """

        if not self.session:
            raise RuntimeError("Session not initialized. Use async with context. ")

        async with self.limiter:
            try:
                async with self.session.get(url, timeout=self.timeout) as response:
                    if response.status == 404 and req == self.ANIME:
                        raise AnimeNotFoundError(query)
                    elif response.status == 404 and req == self.CHARACTER:
                        raise CharacterNotFoundError(query)

                    return await response.text()

            except aiohttp.ClientError as e:
                raise NetworkError(f"Network error occurred: {e}")
                


    async def get_anime(self, anime_id: str)->Anime:
        """
        Fetch and parse anime details.

        Args:
            anime_id (str): The MyAnimeList ID of the anime.

        Returns:
            Anime: An object containing detailed anime information.
        """
        if self.use_cache:
            if not self.db:
                raise RuntimeError("Database is not initialized")
            cached_data = await _get_from_cache(self.db, "anime", anime_id)
            if cached_data:
                return Anime.model_validate_json(cached_data)

        url = f"{self.BASE_URL}/anime/{anime_id}"
        html = await self._fetch(url, self.CHARACTER, anime_id)
        anime =  _parse_anime_data(html)

        if self.use_cache:
            await _store_in_cache(self.db, "anime", anime_id, anime.model_dump_json())

        return anime



    async def get_character(self, character_id: str)-> Character:
        """
        Fetch and parse character details.

        Args:
            character_id (str): The MyAnimeList ID of the character.

        Returns:
            Character: An object containing detailed character information.
        """
        
        if self.use_cache:
            if not self.db:
                raise RuntimeError("Database is not initialized")
            cached_data = await _get_from_cache(self.db, "character", character_id)
            if cached_data:
                return Character.model_validate_json(cached_data)

        url = f"{self.BASE_URL}/character/{character_id}"
        html = await self._fetch(url, self.CHARACTER, character_id)
        character = parse_the_character(html)

        if self.use_cache:
            await _store_in_cache(self.db, "character", character_id, character.model_dump_json())
        return character


    async def search_anime(self, query: str):
        """
        Search anime by name in myanimelist.net

        Args:
            query (str): The name of the anime.

        Returns:
            Anime: An Anime object with Anime Details.
        """
        url = f"{self.BASE_URL}/anime.php?q={quote(query)}&cat=anime"
        html = await self._fetch(url, self.ANIME, query)
        start = '<table border="0" cellpadding="0" cellspacing="0" width="100%">'
        end = '<td class="borderClass bgColor1" valign="top" width="50">'

        # spliting and getting table contents remove useless codes
        anime_lists = "".join(html.split(start)[1].split(end, 9)[1:-1])
        # ((anime name, anime url)) tuple
        allanime = parse_anime_search(anime_lists)
        animeNames = tuple((x[0] for x in allanime))

        matched = get_close_match(query, animeNames)
        # if match rate > 50 return matched anime else first anime from list
        index = matched[2] if matched[1] > 60 else 0
        url = allanime[index][1]
        return await self.get_anime(get_id(url).strip())




    async def search_character(self, query: str):
        """
        Search Character by name in myanimelist.net

        Args:
            query (str): The name of the Character.

        Returns:
            Character: A Character object with The Character Details.
        """

        url = f"{self.BASE_URL}/character.php?q={query}&cat=character"
        html = await self._fetch(url, self.CHARACTER, query)
        start = '<table border="0" cellpadding="0" cellspacing="0" width="100%">'
        end = '</table>'
        # getting all the Character row from table of search results
        table = html.split(start)[1].split(end)[0].split('width="175">', 8)
        chars = tuple((parse_character_search(x) for x in table))
        names = tuple((normalize(x[0]) for x in chars))

        # if match rate higher than 50 return match else first char
        matched = get_close_match(query, names)
        index = matched[2] if matched[1] > 50 else 0
        url = chars[index][1]
        return await self.get_character(get_id(url))



    async def search_batch_anime(self, anime_names: List)-> List[Anime]:
        """
        Fetches multiple anime in batch.

        Args:
            anime_names (List): List of anime names.

        Returns:
            List[Anime]: Returns a list of Anime class object with anime details.

        """

        tasks = [asyncio.create_task(self.search_anime(name)) for name in anime_names]
        animes = await asyncio.gather(*tasks)
        return [anime for anime in animes]

    
    async def search_batch_character(self, character_names: List)-> List[Character]:
        """
        Fetches multiple characters in batch.

        Args:
            character_names (List): List of character names.

        Returns:
            List[Character]: Returns a list of Anime class object with anime details.

        """

        tasks = [asyncio.create_task(self.search_character(name)) for name in character_names]
        characters = await asyncio.gather(*tasks)
        return [anime for anime in characters]
