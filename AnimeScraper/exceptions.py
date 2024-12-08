"""
AnimeScraper Exception classes
"""
class AnimeScraperError(Exception):
    """Base class for all custom exceptions in AnimeScraper."""
    pass


class AnimeNotFoundError(AnimeScraperError):
    """Raised when an anime is not found on MyAnimeList."""
    def __init__(self, anime_name: str):
        super().__init__(f"\x1b[38;5;124mAnime with id/name\x1b[0m \x1b[38;5;220m'{anime_name}'\x1b[0m \x1b[38;5;124mnot found on MyAnimeList.\x1b[0m")


class CharacterNotFoundError(AnimeScraperError):
    """Raised when a character is not found on MyAnimeList."""
    def __init__(self, character_name: str):
        super().__init__(f"\x1b[38;5;124mCharacter with id/name\x1b[0m '{character_name}'\x1b[0m \x1b[38;5;124mnot found on MyAnimeList.\x1b[0m")


class NetworkError(AnimeScraperError):
    """Raised when there is a network-related issue."""
    def __init__(self, message: str = "\x1b[38;5;124mA network error occurred.\x1b[0m"):
        super().__init__(message)

