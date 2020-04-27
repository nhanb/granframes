import wikitextparser as wtp
from requests import get

CHAR_NAMES = [
    "Beelzebub",
    "Charlotta",
    "Djeeta",
    "Ferry",
    "Gran",
    "Katalina",
    "Ladiva",
    "Lancelot",
    "Lowain",
    "Metera",
    "Narmaya",
    "Percival",
    "Soriz",
    "Vaseraga",
    "Zeta",
    "Zooey",
]


def get_character_data(name) -> wtp.WikiText:
    """
    Dustloop wiki uses the Labeled Section Transclusion plugin to generate character
    pages from raw wikitext:
        https://www.dustloop.com/wiki/index.php?title=Help:Editing_Frame_Data

    Luckily, wikemedia exposes an API to get that raw data, and there's already a
    wikitext parser in Python, so no manual parsing is required.
    """
    resp = get(
        "https://www.dustloop.com/wiki/api.php",
        params={
            "action": "query",
            "prop": "revisions",
            "rvprop": "content",
            "format": "json",
            "titles": f"GBVS/{name}/Data",
        },
    ).json()
    raw_data = list(resp["query"]["pages"].values())[0]["revisions"][0]["*"]
    return wtp.parse(raw_data)


FIELDS = [
    "damage",
    "level",
    "attribute",
    "guard",
    "startup",
    "active",
    "recovery",
    "onBlock",
    "onHit",
    "blockstun",
    "groundHit",
    "airHit",
    "hitstop",
    "invul",
    "hitbox",
]


def to_json(wt: wtp.WikiText) -> dict:
    result = {}
    title_suffix = " Data"
    sections = (s for s in wt.sections if s.title.endswith(title_suffix))
    for section in sections:
        section_data = None
        for template in section.templates:
            if template.normal_name() == "FrameData-GBVS":
                section_data = {
                    arg.name: arg.value.strip()
                    for arg in template.arguments
                    if arg.value.strip()
                }
                key = section.title[: -len(title_suffix)]
                if key in result:
                    raise Exception("Unpexpected duplicate section title: " + key)
                result[key] = section_data
                break

    return result


def all_chars():
    results = {}
    for name in CHAR_NAMES:
        print("Fetching", name)
        raw = get_character_data(name)
        parsed = to_json(raw)
        results[name] = parsed
    return results
