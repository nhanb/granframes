from enum import Enum, unique

import wikitextparser as wtp
from requests import get


@unique
class Name(Enum):
    DJE = "Djeeta"
    BEE = "Beelzebub"
    ZOO = "Zooey"
    NAR = "Narmaya"
    FER = "Ferry"
    GRA = "Gran"
    LAN = "Lancelot"
    PER = "Percival"
    KAT = "Katalina"
    MET = "Metera"
    SOR = "Soriz"
    LAD = "Ladiva"
    CHA = "Charlotta"
    ZET = "Zeta"
    VAS = "Vaseraga"
    LOW = "Lowain"


def get_character_data(name: Name) -> wtp.WikiText:
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
            "titles": f"GBVS/{name.value}/Data",
        },
    ).json()
    raw_data = list(resp["query"]["pages"].values())[0]["revisions"][0]["*"]
    return wtp.parse(raw_data)
