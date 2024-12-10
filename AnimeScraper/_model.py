"""
Data models for AnimeScraper.

This module defines data structures for anime, characters, and related entities.
"""
from typing import Optional, List, Dict
#from dataclasses import dataclass 
from pydantic import BaseModel


class AnimeCharacter(BaseModel):
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

    # def _to_dict(self):
    #     return self.__dict__
    #
    # @classmethod
    # def _from_dict(cls, data: dict):
    #     return cls(**data)
    #

class Character(BaseModel):
    """
    Represents a character with full details.

    Attributes:
        id (str): The character's ID.
        name (str): The character's name.
        japanese_name (str): The character's Japanese name.
        about (Dict): A dictionary containing The character's Age, Height, Weight etc.
        description (str): The character's description from MAL.
        img (str): Character image.
        favorites (str): The number people marked it as favorite
        url (str): The MAL Page url of the Character.
    """
    id: str
    name: str
    japanese_name: Optional[str]
    about: Dict[str, str]
    description: str
    img: str
    favorites: str
    url: str

    # def _to_dict(self):
    #     return self.__dict__
    #
    # @classmethod
    # def _from_dict(cls, data: dict):
    #     return cls(**data)

class AnimeStats(BaseModel):
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
    members: str
    favorites: str

    # def _to_dict(self):
    #     return self.__dict__
    #
    # @classmethod
    # def _from_dict(cls, data: dict):
    #     return cls(**data)
    #

class Anime(BaseModel):
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
        studios (str): List of studios.
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
    genres: List[str]
    studios: str
    themes: List[str]
    stats: AnimeStats
    characters: List[AnimeCharacter]


    # def _to_dict(self):
    #     return {
    #         **self.__dict__,
    #         "stats": self.stats.__dict__,
    #         "characters": [c._to_dict() for c in self.characters]
    #     }
    #
    # @classmethod
    # def _from_dict(cls, data: dict):
    #     stats = AnimeStats._from_dict(data["stats"])
    #     characters = [AnimeCharacter._from_dict(char) for char in data["characters"]]
    #     return cls(
    #         id=data["id"],
    #         title=data["title"],
    #         english_title=data["english_title"],
    #         japanese_title=data["japanese_title"],
    #         anime_type=data["anime_type"],
    #         episodes=data["episodes"],
    #         status=data["status"],
    #         aired=data["aired"],
    #         duration=data["duration"],
    #         premiered=data["premiered"],
    #         rating=data["rating"],
    #         synopsis=data["synopsis"],
    #         genres=data["genres"],
    #         studios=data["studios"],
    #         themes=data["themes"],
    #         stats=stats,
    #         characters=characters,
    #     )
    #
