from fastapi import FastAPI, HTTPException, Depends, Query
from AnimeScraper import KunYu  # Import KunYu (main entry point)
from AnimeScraper._model import Anime, Character  # Import response models
from typing import Generator, List
import asyncio, os

app = FastAPI(
    title="AnimeScraper API", 
    description="API for interacting with MyAnimeList data using AnimeScraper", 
    version="1.1.1"
)

USE_CACHE = os.getenv("ANIME_SCRAPER_USE_CACHE", "False") == "True"
DB_PATH = os.getenv("ANIME_SCRAPER_DB_PATH", "cache.db")
# Dependency to provide KunYu instance
# For resuing session :)
def get_kunyu_instance() -> Generator[KunYu, None, None]:
    """
    Dependency to manage KunYu instance and session.
    Ensures the session is created once and reused across requests.
    """

    kunyu_instance = KunYu(use_cache=USE_CACHE, db_path=DB_PATH, max_requests=3)  # Reusing session across requests
    yield kunyu_instance
    # Clean up and close the session once the app shuts down
    if kunyu_instance.shared_session:
        asyncio.run(kunyu_instance.shared_session.close())
        print("✅ KunYu instance closed successfully!")


@app.get("/anime/{anime_id}", response_model=Anime)
async def get_anime(anime_id: str, kunyu_instance: KunYu = Depends(get_kunyu_instance)) -> Anime:
    """
    Endpoint to get anime details by its MAL ID.
    """
    try:
        anime = await kunyu_instance.get_anime(anime_id)
        if anime is None:
            raise HTTPException(status_code=404, detail="Anime not found")
        return anime
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching anime: {str(e)}")


@app.get("/character/{character_id}", response_model=Character)
async def get_character(character_id: str, kunyu_instance: KunYu = Depends(get_kunyu_instance)) -> Character:
    """
    Endpoint to get character details by its MAL ID.
    """
    try:
        character = await kunyu_instance.get_character(character_id)
        if character is None:
            raise HTTPException(status_code=404, detail="Character not found")
        return character
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error fetching character: {str(e)}")


@app.get("/search-anime/{anime_name}", response_model=Anime)
async def search_anime(anime_name: str, kunyu_instance: KunYu = Depends(get_kunyu_instance)) -> Anime:
    """
    Endpoint to search for anime by name.
    """
    try:
        anime = await kunyu_instance.search_anime(anime_name)
        if anime is None:
            raise HTTPException(status_code=404, detail="Anime not found")
        return anime
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error searching anime: {str(e)}")


@app.get("/search-character/{character_name}", response_model=Character)
async def search_character(character_name: str, kunyu_instance: KunYu = Depends(get_kunyu_instance)) -> Character:
    """
    Endpoint to search for a character by name.
    """
    try:
        character = await kunyu_instance.search_character(character_name)
        if character is None:
            raise HTTPException(status_code=404, detail="Character not found")
        return character
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error searching character: {str(e)}")



@app.get("/search-batch-anime/", response_model=List[Anime])
async def search_batch_anime(
    anime_names: List[str] = Query(..., description="List of anime names to search", alias="anime_names[]"),
    kunyu_instance: KunYu = Depends(get_kunyu_instance)
) -> List[Anime]:
    """
    Search for multiple anime by name.

    Args:
        anime_names (List[str]): List of anime names to search.

    Returns:
        List[Anime]: A list of anime details for the searched names.
    """
    try:
        print(f"Searching batch anime for: {anime_names}")
        animes = await kunyu_instance.search_batch_anime(anime_names)
        if not animes:
            raise HTTPException(status_code=404, detail="No anime found for batch search")
        return animes
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error batch searching anime: {str(e)}")





@app.get("/search-batch-character/", response_model=List[Character])
async def search_batch_character(
    character_names: List[str] = Query(..., description="List of character names to search", alias="character_names[]"),
    kunyu_instance: KunYu = Depends(get_kunyu_instance)
) -> List[Character]:
    """
    Search for multiple character by name.

    Args:
        character_names (List[str]): List of character names to search.

    Returns:
        List[Character]: A list of character details for the searched names.
    """
    try:
        print(f"Searching batch character for: {character_names}")
        character = await kunyu_instance.search_batch_character(character_names)
        if not character:
            raise HTTPException(status_code=404, detail="No character found for batch search")
        return character
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error batch searching character: {str(e)}")


