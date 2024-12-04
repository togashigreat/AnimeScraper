from bs4 import BeautifulSoup
from typing import Dict, List, Any 

async def _parse_anime_data(html: str)-> Dict[str, Any]:

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
    
    return {
        "id" : anime_id,
        "title" : title,
        "english_title": eng_title,
        "japanese_title" : jap_title,
        "anime_type": anime_type,
        "episodes": episodes,
        "status" : status,
        "aired" : aired,
        "duration": duration,
        "premiered" : premiered,
        "rating" : rating,
        "synopsis" : synopsis,
        "genres" : genres_list,
        "studios" : studios,
        "themes": theme_list,
        "stats": anime_stats,
        "characters": anime_characters
    }
    


async def get_anime_stats(soup: BeautifulSoup)-> List[str]:
    score = soup.find("span", attrs={"itemprop": "ratingValue"}).text #type: ignore
    scored_by = soup.find("span", attrs={"itemprop": "ratingCount"}).text #type: ignore
    popularity = get_span_text(soup, "Popularity")
    members = get_span_text(soup, "Members")
    favorites = get_span_text(soup, "Favorites")
    ranked = soup.find("span", "numbers ranked").strong.text # type: ignore
    return [
        score,
        scored_by, # scored by nunbers of people
        ranked,
        popularity,
        members,
        favorites,
    ]


async def _anime_characters(soup)-> List[List]:

    tables = soup.find("div", "detail-characters-list clearfix").find_all("table", attrs={"width":"100%"}) #type: ignore    
    characters = []

    for table in tables:
        character = table.find("h3", "h3_characters_voice_actors")
        td_tag = table.find("td", "va-t ar pl4 pr4")
        characters.append([
            get_id(character.a.get("href")), # character id
            remove_coma(character.a.text),   # character name
            character.parent.small.text,     # character role
            get_voice_actor(table)           # voice actor information
            ])        
    return characters


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



async def get_character(html: str)-> List:
    start = '<h2 class="normal_header" style="height: 15px;">'
    end = '<div class="normal_header">'

    #spliting to get the part where the informations are
    main_content = html.split(start)[1].split(end)[0]

    text_lines = BeautifulSoup(main_content, "html.parser").get_text(separator="\n", strip=True).strip().splitlines()
    
    name = text_lines[0]
    japanese_name = text_lines[1][1:-1]
    id = BeautifulSoup(html, "html.parser").find("meta", {"property":"og:url"}).get("content") #type: ignore

    return [
        get_id(id),
        name,
        japanese_name,
        extract_character_bio(text_lines)
        ]

def extract_character_bio(text_lines):

    attributes = ("Age", "Birthday", "Height", "Weight", "Eye Color", "Blood Type","Occupation", "Team")
    bio = {
        key: value.strip()
        for line in text_lines if ":" in line and (key := line.split(":")[0].strip()) in attributes
        for value in line.split(":")[1:]
        }
    return bio


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


def parse_anime_search(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("a", "hoverinfo_trigger fw-b fl-l")
    
    name = tag.text #type: ignore
    url = tag.get("href") #type: ignore

    return (name, url)

