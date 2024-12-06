from AnimeScraper import KunYu
import asyncio

async def main():
    #    scraper = KunYu()
    animes = ["Violet Eveegarden", "dr stone", "The pet girl of sakurasou"]
    async with KunYu() as scraper:
        anime_lists = await scraper.search_batch_anime(animes)
    print(anime_lists[2].title)


asyncio.run(main())
