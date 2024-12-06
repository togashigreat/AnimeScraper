Sync Usage
==========

Here's how you can use the AnimeScraper synchronously.

Searching Anime
~~~~~~~~~~~~~~~

.. code-block:: python

  from AnimeScraper import SyncKunYu

  scraper = SyncKunYu()
  anime = scraper.search_anime("Chuunibyo demo koi ga shita")

  print(anime.title)
  print(anime.stats.rank)


Searching Character
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  from AnimeScraper import SyncKunYu

  scraper = SyncKunYu()
  character = scraper.search_character("Yuu Otosaka")

  print(character.name)
  print(character.about)



.. Note:: To get the exact chataracter you want use the correct name of the character. Otherwise, It may show you a different character's result.


Fetching Anime by ID
~~~~~~~~~~~~~~~~~~~~

.. Note:: The `id` refers to the id of the anime from MAL website.


.. code-block:: python

  from AnimeScraper import SyncKunYu

  scraper = SyncKunYu()
  # remeber the id must be in str format
  anime = scraper.get_anime("1")

  print(anime.synopsis)
  print(anime.characters)


Fetching Character by ID
~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

  from AnimeScraper import SyncKunYu

  scraper = SyncKunYu()
  character = scraper.get_character("1")

  print(character.about)
  print(character.description)

