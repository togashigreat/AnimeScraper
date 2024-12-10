import re
from bs4 import BeautifulSoup
from typing import Dict, List
from ._model import Anime, AnimeCharacter, AnimeStats, Character
from rapidfuzz import process, fuzz
from .exceptions import CharacterNotFoundError

def _parse_anime_data(html: str)-> Anime:

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
    theme_list = [i.string for i in theme.parent.find_all("a")] if theme else ["N/A"] # type: ignore 
    
    genres = soup.find("span", "dark_text", string="Genres:")
    if genres == None:
        genres = soup.find("span", "dark_text", string="Genre:")
    genres_list = [a.string for a in genres.parent.find_all("a")] if genres else ["N/A"]  # type: ignore 

    anime_stats = get_anime_stats(soup)
    anime_characters = _anime_characters(soup)

    return Anime(
        id=anime_id,
        title=title,
        english_title=eng_title,
        japanese_title=jap_title,
        anime_type=anime_type,
        episodes=episodes,
        status=status,
        aired=aired,
        duration=duration,
        premiered=premiered,
        rating=rating,
        synopsis=synopsis,
        genres=genres_list,
        studios=studios,
        themes=theme_list,
        stats=anime_stats,
        characters=anime_characters
    )



def get_anime_stats(soup: BeautifulSoup)-> AnimeStats:
    score = soup.find("span", attrs={"itemprop": "ratingValue"}).text #type: ignore
    scored_by = soup.find("span", attrs={"itemprop": "ratingCount"}).text #type: ignore
    popularity = get_span_text(soup, "Popularity")
    members = get_span_text(soup, "Members")
    favorites = get_span_text(soup, "Favorites")
    ranked = soup.find("span", "numbers ranked").strong.text # type: ignore
    return AnimeStats(
        score=score, 
        scored_by=scored_by, 
        ranked=ranked, 
        popularity=popularity, 
        members=members, 
        favorites=favorites
    )


def _anime_characters(soup)-> List[AnimeCharacter]:

    tables = soup.find("div", "detail-characters-list clearfix").find_all("table", attrs={"width":"100%"}) #type: ignore    
    characters = []

    for table in tables:
        character = table.find("h3", "h3_characters_voice_actors")

        characters.append({
            "id": get_id(character.a.get("href")), # character id
            "name": remove_coma(character.a.text),   # character name
            "role": character.parent.small.text,     # character role
            "voice_actor": get_voice_actor(table)           # voice actor information
            })
    
    return [AnimeCharacter.model_validate(c) for c in characters]


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


def parse_anime_search(html)-> List:
    soup = BeautifulSoup(html, "html.parser")
    data = [
        [tag.text, tag.get("href")] for tag in soup.find_all("a", "hoverinfo_trigger fw-b fl-l")
    ]

    return data

def parse_character_search(html)-> tuple:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("a")
    name = tag.text #type: ignore
    url = tag.get("href") #type: ignore
    return (name, url)


def parse_the_character(html):
    # Htto response code: 200 though invalid id/name was given 
    # Check html before parsing
    if '<div class="badresult">Invalid ID provided.</div>' in html:
        raise CharacterNotFoundError("The MAL Character id is Invalid")

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
        id=get_id(url),
        name=name,
        japanese_name=japanese_name,
        about=about,
        description=description,
        img=img, #type: ignore
        favorites=member_favorites,
        url=url #type: ignore
    )

def typ(url: str)-> str:
    """Returns TYPE from url anime, character etc."""
    if "cat=" in url:
        return "".join(url.split("=")[-1])
    else:
        return "".join(url.split("https://myanimelist.net/")[1].split("/")[0])

def normalize(text)-> str:
    return re.sub(r"[^a-zA-Z0-9\s]", "", text).lower()


def get_close_match(query, lists):
    return process.extractOne(normalize(query), lists, scorer=fuzz.ratio)


