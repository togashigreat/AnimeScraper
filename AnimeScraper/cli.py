import click
import asyncio
from . import KunYu 
from .exceptions import AnimeNotFoundError, CharacterNotFoundError
S = "\x1b[38;5;33m"
E = "\x1b[0m"
VA = "\x1b[38;5;203m"

@click.group()
def cli():
    """AnimeScraper - CLI to fetch and search anime/character details from MyAnimeList."""
    pass

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

# Add all commands to the CLI
cli.add_command(search_anime)
cli.add_command(search_character)
cli.add_command(get_anime)
cli.add_command(get_character)


if __name__ == '__main__':
    cli()

