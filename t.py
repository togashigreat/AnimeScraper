from AnimeScraper import KunYu
import asyncio
async def m():
    s = KunYu()
    anime = await s.search_anime("Clannad")
    print(anime.stats)

asyncio.run(m())
