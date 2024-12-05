import re
from bs4 import BeautifulSoup
from typing import Dict, List
from ._model import Anime, AnimeCharacter, AnimeStats, Character
async def _parse_anime_data(html: str)-> Anime:

    soup = BeautifulSoup(html, "html.parser")
    anime_id = soup.find("input", attrs={"name": "aid"}).attrs["value"] # type: ignore

    title = soup.find("h1", "title-name h1_bold_none").text # type: ignore
    jap_title = get_span_text(soup, "Japanese") 
    eng_title = get_span_text(soup, "English")
    anime_type = get_span_text(soup, "Type")
    episodes = get_span_text(soup, "Episodes")
    duration = get_span_text(soup, "Duration")
    status = get_span_text(soup, "Status")
    aired = get_span_text(soup, "Aired")
    premiered = get_span_text(soup, "Premiered")
    studios = get_span_text(soup, "Studios")
    rating = get_span_text(soup, "Rating")
    synopsis = soup.find_all("p", attrs={'itemprop': 'description'})[0].text

    theme = soup.find("span", "dark_text", string="Theme:")  # type: ignore
    if theme == None:
        theme = soup.find("span", "dark_text", string="Themes:")
    theme_list = [i.string for i in theme.parent.find_all("a")] if theme else None # type: ignore 
    
    genres = soup.find("span", "dark_text", string="Genres:")
    if genres == None:
        genres = soup.find("span", "dark_text", string="Genre:")
    genres_list = [a.string for a in genres.parent.find_all("a")] if genres else None # type: ignore 

    anime_stats = await get_anime_stats(soup)
    anime_characters = await _anime_characters(soup)

    return Anime(
        anime_id,
        title,
        eng_title,
        jap_title,
        anime_type,
        episodes,
        status,
        aired,
        duration,
        premiered,
        rating,
        synopsis,
        genres_list,
        studios,
        theme_list,
        anime_stats,
        anime_characters
    )



async def get_anime_stats(soup: BeautifulSoup)-> AnimeStats:
    score = soup.find("span", attrs={"itemprop": "ratingValue"}).text #type: ignore
    scored_by = soup.find("span", attrs={"itemprop": "ratingCount"}).text #type: ignore
    popularity = get_span_text(soup, "Popularity")
    members = get_span_text(soup, "Members")
    favorites = get_span_text(soup, "Favorites")
    ranked = soup.find("span", "numbers ranked").strong.text # type: ignore
    return AnimeStats(
        score, 
        scored_by, 
        ranked, 
        popularity, 
        members, 
        favorites
    )


async def _anime_characters(soup)-> List[AnimeCharacter]:

    tables = soup.find("div", "detail-characters-list clearfix").find_all("table", attrs={"width":"100%"}) #type: ignore    
    characters = []

    for table in tables:
        character = table.find("h3", "h3_characters_voice_actors")
        characters.append([
            get_id(character.a.get("href")), # character id
            remove_coma(character.a.text),   # character name
            character.parent.small.text,     # character role
            get_voice_actor(table)           # voice actor information
            ])
    
    return [AnimeCharacter(*c) for c in characters]


def get_voice_actor(table)-> Dict[str, str]:
    td_tag = table.find("td", "va-t ar pl4 pr4")
    if td_tag:
        return {

            "id": get_id(td_tag.a.get("href")), # voice actor MAL ID 
            "name": remove_coma(td_tag.a.text), # voice actor name
            "role": td_tag.small.text,
            "url": td_tag.a.get("href") #voice actor information page url
        }
    return {"id": "N/A","name": "N/A", "role": "N/A", "url": "N/A"}



def remove_coma(name: str):
    return "".join(name.split(",")) # Name has coma. ex: "Togashi, Yuuta"


def get_id(url):
    """Get ID of character/people/anime fron URL"""
    return url.split("https://myanimelist.net/")[1].split("/")[1]


def get_span_text(soup: BeautifulSoup, info_name: str)->str:
    if soup.find("span", "dark_text", string=f"{info_name}:"):
        return soup.find("span", "dark_text", string=f"{info_name}:").parent.text.strip().split(f"{info_name}:")[-1].strip() # type: ignore 
    else:
        return "N/A"


def parse_anime_search(html)-> tuple:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("a", "hoverinfo_trigger fw-b fl-l")
    
    name = tag.text #type: ignore
    url = tag.get("href") #type: ignore

    return (name, url)

def parse_character_search(html)-> tuple:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("a")
    name = tag.text #type: ignore
    url = tag.get("href") #type: ignore
    return (name, url)


async def parse_the_character(html):

    soup = BeautifulSoup(html, "html.parser")
    url = soup.find("meta", {"property":"og:url"}).get("content") #type: ignore
    img = soup.find("meta", {"property": "og:image"}).get("content") #type: ignore
    match = re.search(r"Member Favorites:\s*([\d,]+)", soup.get_text())
    # Remove commas for integer conversion
    member_favorites = match.group(1).replace(",", "")  #type: ignore
    start = '<h2 class="normal_header" style="height: 15px;">'
    end = '<div class="normal_header">'

    html = html.split(start)[1].split(end)[0]
    soup = BeautifulSoup(html, "html.parser")

    for spoiler in soup.find_all("div", "spoiler"):
        spoiler.decompose()

    cleaned_text = str(soup)
    pattern = r".*?:\s*<br\s*/?>\n?"  # Matches "Text: <br>" or "Text:<br/>" followed by an optional newline
    cleaned_text = re.sub(pattern, "", cleaned_text)
    soup = BeautifulSoup(cleaned_text, "html.parser")


    # removing <br> to prepare `about` dictionary
    clean_content = "".join(cleaned_text.split("<br/>"))
    soup_for_texts = BeautifulSoup(clean_content, "html.parser")

    # spliting to get the names and character `about`
    lines = soup_for_texts.get_text("\n").splitlines()
    name, japanese_name = lines[0], lines[1]

    # dictionary may contain age, height, Weight etc.
    about = {
        key: value.strip() for line in lines if ":" in line and len(line) <40 and "(Source" not in line for key, value in [line.split(':')]
    }
    # spliting the soup for character description
    pure_texts = soup_for_texts.get_text(strip=True)

    #getting last item of dict to split description
    k, v = next(reversed(about.items()))
    # last_item = f'{k}: {v}'
    description = "".join(pure_texts.split(f'{k}: {v}')[1:]).strip()

    return Character(
        get_id(url),
        name,
        japanese_name,
        about,
        description,
        img, #type: ignore
        member_favorites,
        url #type: ignore
    )

