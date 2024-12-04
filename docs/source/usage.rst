Usage Guide
===========

Basic Usage
-----------
Here’s how you can use the AnimeScraper library:




Fetching Anime Details
~~~~~~~~~~~~~~~~~~~~~~
To fetch details of an anime:

.. code-block:: python
   
  # example 0
  import asyncio 
  from AnimeScraper import KunYu
  
  async def main():
      scraper = KunYu()
      anime = await scraper.search_anime("Bungo stray dog 2 seasn")  # Fetching Bungou Stray Dogs 2nd season anime details
      print(anime.title)
      print(anime.episodes)
   
  asyncio.run(main())



Fetching Anime Details
~~~~~~~~~~~~~~~~~~~~~~
To fetch details of an anime:

.. code-block:: python
   
  # example 1
  import asyncio 
  from AnimeScraper import KunYu
  
  async def main():
    async with KunYu() as scraper:
      anime = await scraper.get_anime("1")  # Replace `1` with a valid anime ID
      print(anime.title)
      print(anime.episodes)
   
  asyncio.run(main())

Fetching Character Details
~~~~~~~~~~~~~~~~~~~~~~~~~~
To fetch details of a character:

.. code-block:: python

   #example 2
   import asyncio
   from AnimeScraper import KunYu

   async def main():
      scraper = KunYu()
      character = await scraper.get_character("1")  # Replace `1` with a valid character ID
      print(character.name)

   asyncio.run(main())


.. Note:: You can use ``KunYu()`` class with async conext manager like **example 1** or you can normally define ``KunYu()`` to a variable as we did in **example 2** and in **example 0** whatever you lke. 

