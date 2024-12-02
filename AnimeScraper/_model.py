"""
Data models for AnimeScraper.

This module defines data structures for anime, characters, and related entities.
"""
from typing import Optional, List, Dict
from dataclasses import dataclass 

@dataclass
class AnimeCharacter:
    """
    Represents a character in an anime.

    Attributes:
        id (str): The character's ID.
        name (str): The character's name.
        role (Optional[str]): The character's role in the anime.
        voice_actor (Dict[str, str]): Details about the voice actor.
    """
    id: str
    name: str
    role: Optional[str]
    voice_actor: Dict[str, str]

@dataclass 
class Character:
    """
    Represents a character in an anime with full details.

    Attributes:
        id (str): The character's ID.
        name (str): The character's name.
        japanese_name (str): The character's Japanese name.
        information (Dict): A dictionary containing The character's Age, Height, Weight etc.
    """
    id: str
    name: str
    japanese_name: Optional[str]
    information: Dict


@dataclass
class AnimeStats:
    """
    Represents The stats of an Anime.

    Attributes:
        score (str): The Anime's score.
        scored_by (str): scored by the number of poeple.
        ranked (str): The rank of The Anime.
        popularity (str): The popularity of the Anime.
        favorites (stt): The number of poeple marked it as their favorite Anime.
    """

    score: str
    scored_by: str
    ranked: str
    popularity: str
    memebers: str
    favorites: str


@dataclass 
class Anime:
    """
    Represents an anime.

    Attributes:
        id (str): The anime's ID.
        title (str): The anime's title.
        english_title (Optional[str]): The English title of the anime.
        japanese_title (Optional[str]): The Japanese title of the anime.
        anime_type (str): The type of anime (e.g., TV, Movie).
        episodes (Optional[str]): Number of episodes.
        status (str): The current status (e.g., Finished Airing).
        aired (str): The airing date range.
        duration (str): Average duration of an episode.
        rating (str): The age rating (e.g., PG-13).
        synopsis (str): A brief synopsis of the anime.
        genres (List[str]): List of genres.
        studios (List[str]): List of studios.
        themes (List[str]): List of themes.
        stats (AnimeStats): Statistics about the anime.
        characters (List[AnimeCharacter]): List of characters in the anime.
    """

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

