Async Usage
===========

Here's how you can use AnimeScraper asynchronously.


Searching Anime
~~~~~~~~~~~~~~~~~~~~~~~~~~
To Search and fetch details of an anime:

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



Searching Character
~~~~~~~~~~~~~~~~~~~~~~~~~~
To Search and fetch details of a Character:

.. code-block:: python
   
  # example 1
  import asyncio 
  from AnimeScraper import KunYu
  
  async def main():
      scraper = KunYu()
      character = await scraper.search_character("Togashi Yuuta")  # Searching for the Character Togashi Yuuta
      print(character)
      print(character.japanese_name)
      print(character.about)
      print(character.description)
   
  asyncio.run(main())


.. Note:: To get the exact chataracter you want use the correct name of the character. Otherwise, It may show you a different character's result.


Fetching Anime Details
~~~~~~~~~~~~~~~~~~~~~~
To fetch details of an anime:

.. code-block:: python
   
  # example 2
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

   #example 3
   import asyncio
   from AnimeScraper import KunYu

   async def main():
      scraper = KunYu()
      character = await scraper.get_character("1")  # Replace `1` with a valid character ID
      print(character.name)
      print(character.img)

   asyncio.run(main())


Caching
~~~~~~~~~

If you want to locally cache in storage you can pass ``use_cache = True`` to ``KunYu()`` class. you can specify the database path by passing ``db_path="mycache.db"`` 


.. code-block:: python

   #example 3
   import asyncio
   from AnimeScraper import KunYu

   async def main():
      scraper = KunYu(use_cache=True, db_path="cache.db")
      character = await scraper.get_character("1")
      anime = await scraper.search_anime("The Garden of words")
      print(character.name)
      print(anime.title, anime.id)

   asyncio.run(main())



.. Note:: You can use ``KunYu()`` class with async conext manager like **example 2** or you can normally define ``KunYu()`` to a variable as we did in **example 3** and in **example 0** whatever you lke. 

