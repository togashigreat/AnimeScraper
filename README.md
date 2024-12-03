# AnimeScraper

AnimeScraper is a Python library for effortlessly scraping anime and character data from MyAnimeList.

## 🚀 Features

- Fetch detailed anime information
- Retrieve character details
- Asynchronous data retrieval
- Easy-to-use API
- Fully typed and documented

## 🛠️ Installation

You can install AnimeScraper using pip:

```bash
pip install animescraper
```

## 📖 Quick Start

Fetching Anime details

```python
import asyncio
from AnimeScraper import KunYu

async def main():
    # Use async Context manager to fetch multiple anime with same session
    async with KunYu() as scraper:
        # Fetch anime details by ID
        anime = await scraper.get_anime(32281)  # Fullmetal Alchemist: Brotherhood
        print(anime.title)
        print(anime.synopsis)
        print(anime.stats.score)
        print(anime.characters[0].name)

asyncio.run(main())

```
Fetching Character Details

```python
async def get_character():
    scraper = KunYu()
        # Fetch character details by ID
    character = await scraper.get_character(11)  # Edward Elric
    print(character.name)
    print(character.japanese_name)

asyncio.run(get_character())
```

## 🌟 Key Components

- `KunYu`: Main interface for scraping anime and character data
- `Anime`: Detailed anime information model
- `Character`: Comprehensive character details model
- Asynchronous scraping with `aiohttp`


## 🔧 Requirements

- Python 3.8+
- aiohttp

## 📦 Project Structure

```
AnimeScraper/
│
├── AnimeScraper/
│   ├── Scraper.py       # Main scraping interface
│   ├── _model.py        # Data models
│   ├── malscraper.py    # HTTP connection handler
│   └── _parse_anime_data.py  # HTML parsing utilities
│
├── docs/                # Sphinx documentation
├── tests/               # Unit tests
└── pyproject.toml       # Project configuration
```
## 📄 License

Distributed under the MIT License. See LICENSE for more information.

## 📞 Contact
Contact me - <a href="https://www.facebook.com/KiyotakaO.O?mibextid=ZbWKwL"><img src="https://skillicons.dev/icons?i=instagram" /></a> <br/>

Project Link: <a href="https://github.com/togashigreat/AnimeScraper"><img src="./docs/assets/icon.svg" height="256" width="256" /></a>
