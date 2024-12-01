from typing import Any, Optional, List, Dict
from dataclasses import dataclass 

@dataclass
class AnimeCharacter:
    id: str
    name: str
    role: Optional[str]
    voice_actor: Dict[str, str]

@dataclass 
class Character:
    id: int
    name: str
    japanese_name: Optional[str]
    information: Dict



@dataclass 
class AnimeStaff:
    name: str 
    role: str


@dataclass
class AnimeStats:
    score: str
    scored_by: str
    ranked: str
    popularity: str
    memebers: str
    favorites: str


@dataclass 
class Anime:
    id: str
    title: str
    english_title: Optional[str]
    japanese_title: Optional[str]
    anime_type: str    # TV, Movie, OVA etc.
    episodes: Optional[str]
    status: str       # Airing, Finished, etc.
    aired: str
    duration: str
    premiered: str
    rating: str # PG-13, R, etc.
    synopsis: str
    genres: List[str] | None
    studios: List
    themes: List | None
    stats: AnimeStats
    characters: List[AnimeCharacter]

