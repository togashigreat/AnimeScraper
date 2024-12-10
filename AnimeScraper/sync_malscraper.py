import httpx
from typing import Optional, List 
from urllib.parse import quote 
from concurrent.futures import ThreadPoolExecutor
import sqlite3


from .exceptions import (
    AnimeNotFoundError, 
    CharacterNotFoundError, 
    NetworkError
)
from ._cache_utils import _start_database, _from_cache, _store_cache
from ._parse_anime_data import (
    _parse_anime_data,
    parse_anime_search, 
    parse_the_character,
    parse_character_search,
    get_id,
    get_close_match,
    normalize
)

from ._model import Anime, Character


class SyncMalScraper():

    BASE_URL = "https://myanimelist.net"
    ANIME = 10 
    CHARACTER = 20

    def __init__(
        self, 
        client: Optional[httpx.Client],
        use_cache: bool,
        db_path: str,
        timeout: int
        ) -> None:
        self.client = client
        self.own_client = client is None
        self.use_cache = use_cache
        self.db_path = db_path
        self.db: sqlite3.Connection | None = None
        self.timeout = timeout

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    def __enter__(self):

        if not self.client:
            self.client = httpx.Client(headers=self.headers)

        if self.use_cache:
            _start_database(self.db_path)
            self.db = sqlite3.connect(self.db_path)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client and self.own_client:
            self.client.close()
            self.session = None

        if self.db:
            self.db.close()


    def _fetch(self, url: str, req: int, query: str)-> str:
        
        if not self.client:
            raise ValueError("session is not initialised. Use `with SyncMalScraper` for proper initialisation")
        try:
            response = self.client.get(url, timeout=self.timeout)
            if response.status_code == 404 and self.ANIME == req:
                raise AnimeNotFoundError(query)
            elif response.status_code == 404 and self.CHARACTER == req:
                raise CharacterNotFoundError(query)
            return response.text

        except httpx.NetworkError as e:
            raise NetworkError(f"A NetworkError error occurred {e}")


    def get_anime(self, anime_id: str)->Anime:
        """
        Fetch and parse anime details.

        Args:
            anime_id (str): The MyAnimeList ID of the anime.

        Returns:
            Anime: An object containing detailed anime information.
        """
        if self.use_cache:
            cached_data = _from_cache(self.db, "anime", anime_id)
            if cached_data:
                return Anime.model_validate_json(cached_data)

        url = f"{self.BASE_URL}/anime/{anime_id}"

        html = self._fetch(url, self.ANIME, anime_id)
        anime =  _parse_anime_data(html)
        if self.use_cache:
            _store_cache(self.db, "anime", anime_id, anime.model_dump_json())
        return anime



    def get_character(self, character_id: str)-> Character:
        """
        Fetch and parse character details.

        Args:
            character_id (str): The MyAnimeList ID of the character.

        Returns:
            Character: An object containing detailed character information.
        """
        
        if self.use_cache:
            cached_data = _from_cache(self.db, "character", character_id)
            if cached_data:
                return Character.model_validate_json(cached_data)

        url = f"{self.BASE_URL}/character/{character_id}"
        html = self._fetch(url, self.CHARACTER, character_id)
        character = parse_the_character(html)
        if self.use_cache:
            _store_cache(self.db, "character", character_id, character.model_dump_json())
           
        return character



    def search_anime(self, query: str)-> Anime:

        url = f"{self.BASE_URL}/anime.php?q={quote(query)}&cat=anime"
        html = self._fetch(url, self.ANIME, query)
        start = '<table border="0" cellpadding="0" cellspacing="0" width="100%">'
        end = '<td class="borderClass bgColor1" valign="top" width="50">'

        # spliting and getting table contents remove useless codes
        anime_lists = "".join(html.split(start)[1].split(end, 9)[1:-1])
        # ((anime name, anime url)) tuple
        allanime = parse_anime_search(anime_lists)
        animeNames = tuple((x[0] for x in allanime))

        matched = get_close_match(query, animeNames)
        # if match rate > 50 return matched anime else first anime from list
        index = matched[2] if matched[1] > 50 else 0
        url = allanime[index][1]
        return self.get_anime(get_id(url))



    def search_character(self, query: str)-> Character:
        """
        Search Character by name in myanimelist.net

        Args:
            query (str): The name of the Character.

        Returns:
            Character: A Character object with The Character Details.
        """

        url = f"{self.BASE_URL}/character.php?q={query}&cat=character"
        html = self._fetch(url, self.CHARACTER, query)
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

        return self.get_character(get_id(url))



    def search_batch_anime(self, anime_names: List[str])-> List[Anime]:
        with ThreadPoolExecutor(max_workers=5) as threat:
            results = threat.map(self.search_anime, anime_names)
            return [result for result in results]


    def search_batch_character(self, characters_name: List[str])-> List[Character]:

        characters_lists = [self.search_character(name) for name in characters_name]
        return characters_lists
