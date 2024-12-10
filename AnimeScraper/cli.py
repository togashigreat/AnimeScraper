import os, json
import click
import asyncio
from uvicorn import run as start_server
from . import KunYu 
from .exceptions import AnimeNotFoundError, CharacterNotFoundError


S = "\x1b[38;5;33m"
E = "\x1b[0m"
VA = "\x1b[38;5;203m"

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".kunyu")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def create_default_config():
    """Creates the default config file in ~/.kunyu/config.json if it doesn't exist."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "use_cache": False,
            "db_path": "cache.db",
            "port": 8000,
            "host": "127.0.0.1"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)


def load_config():
    """Loads config from ~/.kunyu/config.json."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

@click.group()
def cli():
    """AnimeScraper - CLI to fetch and search anime/character details from MyAnimeList."""
    create_default_config()


@click.command()
@click.argument('anime_name')
def search_anime(anime_name: str):
    """Search for an anime by name."""
    try:
        async def run():
            async with KunYu() as scraper:
                print(f"\x1b[38;5;45m> Searching for anime\x1b[0m: \x1b[38;5;44m{anime_name}\x1b[0m\n")
                anime = await scraper.search_anime(anime_name)

                click.echo(f"{S}Title{E}: {VA}{anime.title}{E}")
                click.echo(f"{S}Japanese Title{E}: {VA}{anime.japanese_title}{E}")
                click.echo(f"{S}Type{E}: {VA}{anime.anime_type}{E}")
                click.echo(f"{S}Episodes{E}: {VA}{anime.episodes}{E}")
                click.echo(f"{S}Duration{E}: {VA}{anime.duration}")
                click.echo(f"{S}Status{E}: {VA}{anime.status}{E}")
                click.echo(f"{S}Rating{E}: {VA}{anime.rating}{E}")
                click.echo(f"{S}Genres{E}: {VA}{' '.join(anime.genres)}{E}")
                click.echo(f"{S}Themes{E}: {VA}{' '.join(anime.themes)}{E}")
                click.echo(f"{S}Premiered{E}: {VA}{anime.premiered}{E}")
                click.echo(f"{S}Aired{E}: {VA}{anime.aired}{E}")
                click.echo(f"{S}Score{E}: {VA}{anime.stats.score}{E}")
                click.echo(f"{S}Scored by{E}: {VA}{anime.stats.scored_by} people{E}")
                click.echo(f"{S}Popularity{E}: {VA}{anime.stats.popularity}{E}")
                click.echo(f"{S}Ranked{E}: {VA}{anime.stats.ranked}{E}")
                click.echo(f"{S}Synopsis{E}: \x1b[38;5;35m{anime.synopsis[:300]}...\x1b[0m")

        asyncio.run(run())
    except AnimeNotFoundError as e:
        click.echo(f"Error: {e}", err=True)



@click.command()
@click.argument('anime_id')
def get_anime(anime_id: str):
    """Get anime details by anime ID."""
    try:
        async def run():
            async with KunYu() as scraper:
                print(f"\x1b[38;5;45m> Fetching anime details for ID: \x1b[0m: \x1b[38;5;44m{anime_id}\x1b[0m")

                anime = await scraper.get_anime(anime_id)

                genres = " ".join(anime.genres)
                click.echo(f"{S}Title{E}: {VA}{anime.title}{E}")
                click.echo(f"{S}Japanese Title{E}: {VA}{anime.japanese_title}{E}")
                click.echo(f"{S}Type{E}: {VA}{anime.anime_type}{E}")
                click.echo(f"{S}Episodes{E}: {VA}{anime.episodes}{E}")
                click.echo(f"{S}Duration{E}: {VA}{anime.duration}")
                click.echo(f"{S}Status{E}: {VA}{anime.status}{E}")
                click.echo(f"{S}Rating{E}: {VA}{anime.rating}{E}")
                click.echo(f"{S}Genres{E}: {VA}{genres}{E}")
                click.echo(f"{S}Themes{E}: {VA}{' '.join(anime.themes)}{E}")
                click.echo(f"{S}Premiered{E}: {VA}{anime.premiered}{E}")
                click.echo(f"{S}Aired{E}: {VA}{anime.aired}{E}")
                click.echo(f"{S}Score{E}: {VA}{anime.stats.score}{E}")
                click.echo(f"{S}Scored by{E}: {VA}{anime.stats.scored_by} people{E}")
                click.echo(f"{S}Popularity{E}: {VA}{anime.stats.popularity}{E}")
                click.echo(f"{S}Ranked{E}: {VA}{anime.stats.ranked}{E}")
                click.echo(f"{S}Synopsis{E}: \x1b[38;5;35m{anime.synopsis[:300]}...\x1b[0m")
        asyncio.run(run())

    except AnimeNotFoundError as e:
        click.echo(f"Error: {e}", err=True)



@click.command()
@click.argument('character_id')
def get_character(character_id: str):
    """Get character details by character ID."""
    try:
        async def run():
            async with KunYu() as scraper:

                print(f"\x1b[38;5;45m> Fetching character details for ID: \x1b[0m: \x1b[38;5;44m{character_id}\x1b[0m\n")
                character = await scraper.get_character(character_id)

                click.echo(f"{S}Name{E}: {VA}{character.name}{E}")
                click.echo(f"{S}Japanese Name{E}: {VA}{character.japanese_name}")
                for key, value in character.about.items():
                    click.echo(f"{S}{key}{E}: {VA}{value}{E}")
                click.echo(f"{S}Description{E}: \x1b[38;5;35m{character.description[:300]}...{E}")  # Limit the description

        asyncio.run(run())
    except CharacterNotFoundError as e:
        click.echo(f"Eror: {e}")



@click.command()
@click.argument('character_name')
def search_character(character_name: str):
    """Get character details by character name."""
    try: 
        async def run():
            async with KunYu() as scraper:

                print(f"\x1b[38;5;45m> Searching for character\x1b[0m: \x1b[38;5;44m{character_name}\x1b[0m\n")
                character = await scraper.search_character(character_name)

                click.echo(f"{S}Name{E}: {VA}{character.name}{E}")
                click.echo(f"{S}Japanese Name{E}: {VA}{character.japanese_name}")
                for key, value in character.about.items():
                    click.echo(f"{S}{key}{E}: {VA}{value}{E}")
                click.echo(f"{S}Description{E}: \x1b[38;5;35m{character.description[:300]}...{E}")  # Limit the description
        asyncio.run(run())

    except CharacterNotFoundError as e:
        click.echo(f"Eror: {e}")


@click.command()
@click.option("--host", default=None, help="Host for the API server (overrides config.json)")
@click.option("--port", default=None, help="Port for the API server (overrides config.json)")
@click.option("--use-cache", is_flag=True, help="Enable database caching (overrides config.json)")
@click.option("--db-path", default=None, help="Path for the local SQLite cache database (overrides config.json)")
def server(host: str, port: int, use_cache: bool, db_path: str):
    """Start the FastAPI server for AnimeScraper."""
    
    # Load from config file and merge with CLI args
    config = load_config()

    # Override config values with CLI arguments if provided
    final_host = host if host else config.get("host", "127.0.0.1")
    final_port = port if port else config.get("port", 8000)
    final_use_cache = use_cache if use_cache else config.get("use_cache", False)
    final_db_path = db_path if db_path else config.get("db_path", "cache.db")

    click.echo(f"🚀 Starting server on http://{final_host}:{final_port}")
    click.echo(f"📁 Database Path: {final_db_path} | 📦 Use Cache: {final_use_cache}")
    # Pass the user arguments to the server through environment variables
    os.environ["ANIME_SCRAPER_USE_CACHE"] = str(final_use_cache)
    os.environ["ANIME_SCRAPER_DB_PATH"] = final_db_path

    # Run the FastAPI server
    start_server("AnimeScraper.animescraper_server:app", host=final_host, port=int(final_port), reload=True)

        
# Add all commands to the CLI
cli.add_command(search_anime)
cli.add_command(search_character)
cli.add_command(get_anime)
cli.add_command(get_character)
cli.add_command(server)

if __name__ == '__main__':
    cli()



