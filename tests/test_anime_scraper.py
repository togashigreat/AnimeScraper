import pytest
from AnimeScraper.AnimeScraper import KunYu

@pytest.mark.asyncio
async def test_get_anime():
    """
    Test fetching anime details from MyAnimeList.
    """
    async with KunYu() as scraper:
        anime = await scraper.get_anime(1)  # Test with a known anime ID (e.g., ID 1)
        assert anime.id == "1", "Anime ID mismatch"
        assert anime.title, "Title should not be empty"
        assert anime.synopsis, "Synopsis should not be empty"
        assert isinstance(anime.genres, list), "Genres should be a list"

@pytest.mark.asyncio
async def test_get_character():
    """
    Test fetching character details from MyAnimeList.
    """
    async with KunYu() as scraper:
        character = await scraper.get_character(1)  # Test with a known character ID (e.g., ID 1)
        assert character.id == "1", "Character ID mismatch"
        assert character.name, "Character name should not be empty"
        assert isinstance(character.information, dict), "Character information should be a dictionary"

def test_import():
    """
    Test importing the main KunYu class.
    """
    try:
        from AnimeScraper.AnimeScraper import KunYu
    except ImportError:
        pytest.fail("Failed to import KunYu class")

