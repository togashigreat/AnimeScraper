"""
Data models for AnimeScraper.

This module defines data structures for anime, characters, and related entities.
"""

__all__ = [
    "Anime",
    "AnimeCharacter",
    "AnimeStats",
    "Character"
    ]

from typing import Optional, List, Dict
from pydantic import BaseModel





class AnimeCharacter(BaseModel):
    # """
    # Represents a character in an anime.
    #
    # Attributes:
    #     id (str): The MAL ID of the character.
    #     name (str): The name of the character.
    #     role (Optional[str]): The character's role in the anime.
    #     voice_actor (Dict[str, str]): Details about the voice actor.
    # """

    id: str 
    """The MAL ID of the character."""
    name: str 
    """The name of the character. """
    role: Optional[str]
    """The character's role in the anime."""
    voice_actor: Dict[str, str]
    """Dictionary containing details about the voice actor."""



class Character(BaseModel):
    # """
    # Represents a character with full details.
    #
    # Attributes:
    #     id (str): The character's ID.
    #     name (str): The character's name.
    #     japanese_name (str): The character's Japanese name.
    #     about (Dict): A dictionary containing The character's Age, Height, Weight etc.
    #     description (str): The character's description from MAL.
    #     img (str): Character image.
    #     favorites (str): The number people marked it as favorite
    #     url (str): The MAL Page url of the Character.
    #
    # """

    id: str
    """The MAL ID of the character"""
    name: str 
    """The name of the Character."""
    japanese_name: Optional[str]
    """Japanese name of the Character"""
    about: Dict[str, str]
    """A dictionary containing character's details"""
    description: str
    """The description about the character"""
    img: str
    """An url of the character image"""
    favorites: str 
    """The number of MAL users favorite character"""
    url: str 
    """The MAL url of the Character page"""



class AnimeStats(BaseModel):
    # """
    # Represents The stats of an Anime.
    #
    # Attributes:
    #     score (str): The Anime's score.
    #     scored_by (str): scored by the number of poeple.
    #     ranked (str): The rank of The Anime.
    #     popularity (str): The popularity of the Anime.
    #     members (str): The member of the anime.
    #     favorites (stt): The number of poeple marked it as their favorite Anime.
    # """

    score: str 
    """The score of the anime."""
    scored_by: str 
    """Number of people scored the anime."""
    ranked: str 
    """The rank of the anime."""
    popularity: str 
    """popularity of the anime."""
    members: str 
    """The member of the anime."""
    favorites: str 
    """The number people's favorite anime."""




class Anime(BaseModel):
    # """
    # Represents an anime with all its details.
    #
    # Attributes:
    #     id (str): The anime's ID.
    #     title (str): The anime's title.
    #     english_title (Optional[str]): The English title of the anime.
    #     japanese_title (Optional[str]): The Japanese title of the anime.
    #     anime_type (str): The type of anime (e.g., TV, Movie).
    #     episodes (Optional[str]): Number of episodes.
    #     status (str): The current status (e.g., Finished Airing).
    #     aired (str): The airing date range.
    #     duration (str): Average duration of an episode.
    #     premiered (str): The premiered data of the anime.
    #     rating (str): The age rating (e.g., PG-13).
    #     synopsis (str): A brief synopsis of the anime.
    #     genres (List[str]): List of genres.
    #     studios (str): List of studios.
    #     themes (List[str]): List of themes.
    #     producers (List[str]): List of producers.
    #     licensors (List[str]): List of licensors.
    #     stats (AnimeStats): Statistics about the anime.
    #     characters (List[AnimeCharacter]): List of characters in the anime.
    #     related (List[dict[str, str]]): Related anime, movie and manga.
    #
    # """


    id: str 
    """The MAL ID of the anime."""
    title: str 
    """The title of the anime. """
    english_title: Optional[str] 
    """The English title of the anime."""
    japanese_title: Optional[str] 
    """# The Japanese title of the anime."""
    anime_type: str 
    """The type of the anime (e.g., TV, Movie, OVA)."""
    episodes: Optional[str] 
    """Episode number of the anime."""
    status: str 
    """The current status (e.g., Finished Airing)."""
    aired: str 
    """The airing date range."""
    duration: str 
    """Average duration of an episode."""
    premiered: str 
    """The premiered data of the anime."""
    rating: str 
    """The age rating (PG-13, R, etc..)."""
    synopsis: str 
    """The synopsis of the anime."""
    genres: List[str] 
    """The genres of the anime."""
    studios: str 
    """The studios that animated the anime."""
    themes: List[str]
    """The themes of the anime (e.g., school, Isekei)"""
    producers: List[str]
    """The producers of the anime."""
    licensors: List[str] 
    """The licensors of the anime."""
    stats: AnimeStats 
    """Statistics of the anime (score, popularity etc..)."""
    characters: List[AnimeCharacter] 
    """List of characters appearing in anime."""
    related: List[dict[str, str]] 
    """Related works (anime, movies, manga etc.)"""

