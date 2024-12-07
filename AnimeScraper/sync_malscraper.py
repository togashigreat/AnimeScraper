import httpx
from typing import Optional, List 
from urllib.parse import quote 
from concurrent.futures import ThreadPoolExecutor

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

    def __init__(self, client: Optional[httpx.Client] = None) -> None:
        self.client = client
        self.own_client = client is None


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    def __enter__(self):
        if not self.client:
            self.client = httpx.Client(headers=self.headers, timeout=10)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client and self.own_client:
            self.client.close()


    def _fetch(self, url: str)-> str:
        
        if not self.client:
            raise ValueError("session is not initialised. Use `with SyncMalScraper` for proper initialisation")
        response = self.client.get(url)
        if response.status_code == 404:
            raise ValueError(f"No data found with URL: {url}")

        return response.text



    def get_anime(self, anime_id: str)->Anime:
        """
        Fetch and parse anime details.

        Args:
            anime_id (str): The MyAnimeList ID of the anime.

        Returns:
            Anime: An object containing detailed anime information.
        """

        url = f"{self.BASE_URL}/anime/{anime_id}"

        html = self._fetch(url)

        return _parse_anime_data(html)



    def get_character(self, character_id: str)-> Character:
        """
        Fetch and parse character details.

        Args:
            character_id (str): The MyAnimeList ID of the character.

        Returns:
            Character: An object containing detailed character information.
        """

        url = f"{self.BASE_URL}/character/{character_id}"

        html = self._fetch(url)

        character_details = parse_the_character(html)

        return character_details



    def search_anime(self, query: str)-> Anime:

        url = f"{self.BASE_URL}/anime.php?q={quote(query)}&cat=anime"
        html = self._fetch(url)
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
        html = self._fetch(url)
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
