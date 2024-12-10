AnimeScraper CLI
================

The **AnimeScraper CLI** is a command-line tool that allows you to interact with MyAnimeList data directly from your terminal. It provides commands to search for anime, get anime details, search for characters, and much more.


**Usage**:

After you install AnimeScraper, you can use the `animescraper` command like this:



.. code-block:: bash

   animescraper [COMMAND] [OPTIONS]


Available Commands
------------------

The following commands are available in the **AnimeScraper CLI**:

.. list-table::
   :header-rows: 1
   :widths: 15 60

   * - **Command**
     - **Description**
   * - `search-anime`
     - Search for an anime by name.
   * - `get-anime`
     - Get anime details using its MyAnimeList (MAL) ID.
   * - `search-character`
     - Search for a character by name.
   * - `get-character`
     - Get character details using its MyAnimeList (MAL) ID.
   * - `:ref:server`
     - Run a FastAPI server for the AnimeScraper API.



---------------------------------


.. _get-anime:

**1. search-anime**
~~~~~~~~~~~~~~~~~~~


This command searches for an anime by its name and returns a summary of its details.


**Usage**:  

.. code-block:: bash

   animescraper search-anime [ANIME_NAME]


**Example**:  

.. code-block:: bash 

   animescraper search-anime "Naruto"



**Output** (Example):

.. code-block:: bash

  > Searching for anime: Naruto

  Title: Naruto  
  Japanese Title: NARUTO  
  Type: TV  
  Episodes: 220  
  Duration: 23 min. per ep.  
  Status: Finished Airing  
  Rating: PG-13 - Teens 13 or older  
  Genres: Action Adventure Comedy  
  Premiered: Fall 2002  
  Aired: Oct 3, 2002 to Feb 8, 2007  
  Score: 7.97  
  Scored by: 1,678,991 people  
  Popularity: #5  
  Ranked: #143  
  Synopsis: Moments prior to Naruto Uzumaki's birth, a huge demon known as the Kyuubi, the Nine-Tailed Fox, attacked Konohagakure... 


---------------------------------

.. _get-anime:

**2. get-anime**
~~~~~~~~~~~~~~~~

This command retrieves anime details using the anime's **MyAnimeList ID**.  

**Usage**:

.. code-block:: bash

  animescraper get-anime [ANIME_ID]


**Example**:  

.. code-block:: bash

  animescraper get-anime 1



**Output** (Example):


.. code-block:: bash

  > Fetching anime details for ID: 1

  Title: Cowboy Bebop  
  Japanese Title: カウボーイビバップ  
  Type: TV  
  Episodes: 26  
  Duration: 24 min. per ep.  
  Status: Finished Airing  
  Rating: R - 17+ (violence & profanity)  
  Genres: Action Adventure Comedy  
  Premiered: Spring 1998  
  Aired: Apr 3, 1998 to Apr 24, 1999  
  Score: 8.78  
  Scored by: 1,212,345 people  
  Popularity: #42  
  Ranked: #26  
  Synopsis: In the year 2071, humanity has colonized several planets and moons of the solar system...



---------------------------------

.. _search-character:

**3. search-character**
~~~~~~~~~~~~~~~~~~~~~~~

This command searches for a character by name and provides a summary of the character's information.

**Usage**

.. code-block:: bash

   animescraper search-character [CHARACTER_NAME]


**Example**

.. code-block:: bash

   animescraper search-character "Narouto"

.. code-block:: bash

   > Searching for character: Naruto Uzumaki

    Name: Naruto Uzumaki  
    Japanese Name: うずまき ナルト  
    Age: 17 (at start)  
    Height: 166 cm (5'5")  
    Weight: 50.9 kg (112 lbs)  
    Description: Naruto Uzumaki is a young ninja with a dream to    become the Hokage, the leader of his village...  



---------------------------------

.. _get-character:

**2. get-character**
~~~~~~~~~~~~~~~~~~~~


This command retrieves character details using the **MyAnimeList ID** of the character.

**Usage**: 

.. code-block:: bash

  animescraper get-character [CHARACTER_ID]


**Example**:  


.. code-block:: bash

  animescraper get-character 20


**Output** (Example):

.. code-block:: bash

  > Fetching character details for ID: 20

  Name: Edward Elric  
  Japanese Name: エドワード・エルリック  
  Age: 15 (start)  
  Height: 150 cm (4'11")  
  Weight: 45 kg (99 lbs)  
  Description: Edward Elric is the protagonist of the series Fullmetal Alchemist. He is a young prodigy in alchemy and seeks to restore...


---------------------------------

.. _server:

**5. server**
~~~~~~~~~~~~~

This command launches a local **FastAPI server** for the AnimeScraper API. Other programming languages (like **JavaScript**) can send requests to this server to access anime and character data.  

**Usage**:  

.. code-block:: bash

  animescraper server --host [HOST] --port [PORT] --use-cache [True] --db-path [DATABASE_PATH]



**Options**:  

- ``--host`` (default: 127.0.0.1) - The IP address where the server will run.  

- ``--port`` (default: 8000) - The port where the server will be available.  

- ``--use-cache``  - Add this while runing the server if you want to cache locally.

- ``--db-path`` (default: 'cache.db') - Specify the database path.


.. Note::  Only add --use-cache flag if you want to cache locally in your device storage.


**Example**:  

.. code-block:: bash

  animescraper server --host 127.0.0.1 --port 8000 --use-cache --db-path "myanime.db"


This will start a server at **http://127.0.0.1:8000** with **local caching enabled**.  


**Example API Requests**:


1️⃣ **Get Anime by ID**  

.. code-block:: bash

  GET http://127.0.0.1:8000/anime/1 


2️⃣ **Search Anime by Name**  

.. code-block:: bash

  GET http://127.0.0.1:8000/search-anime/Naruto


3️⃣ **Search Batch Anime**

.. code-block:: bash

  GET http://127.0.0.1:8000/search-batch-anime?anime_names=Naruto&anime_names=One+Piece


4️⃣ **Get Character by ID**  

.. code-block:: bash

  GET http://127.0.0.1:8000/character/20


5️⃣ **Search Batch Characters**  

.. code-block:: bash

  GET http://127.0.0.1:8000/search-batch-character?character_names=Naruto+Uzumaki&character_names=Monkey+D.+Luffy


----------------------------


Environment Variables
----------------------

The **AnimeScraper CLI** can also read configuration from a file like **.env** or **.json** for the server.  

**File location**:  

.. code-block:: bash

  ~/.kunyu/config.json


**Example JSON File**:

.. code-block:: json 

  {
    "host": "0.0.0.0",
    "port": 8000,
    "use_cache": true,
    "db_path": "mydata.db",
  }



---------------------------------


Usage Tips
----------

- Use **tab completion** to auto-complete commands.  
- Run ``animescraper --help`` to see all available commands.  
- Combine the **server** with API testing using Postman, JavaScript, or Python requests.  

---

FAQ
---

**Q: How do I search for multiple anime at once?**  
A: Use the **batch search** with this command:  

.. code-block:: bash

  animescraper server --use-cache


Then send an HTTP request to:  

.. code-block:: bash

  http://127.0.0.1:8000/search-batch-anime/?anime_names=Naruto&anime_names=One+Piece


**Q: How do I store anime data in the local cache?**

A: Start the server with ``--use-cache`` and it will cache anime/character data locally in SQLite.  

----------------------------------

**Congratulations!** 🎉  
You are now ready to **master the AnimeScraper CLI**. Feel free to explore and use it in your terminal or API server.


---------------------------------

This **Sphinx-styled documentation** is simple, clear, and **easy to read**. Let me know if you'd like to add or customize any sections.

