from pathlib import Path
import json

def token_mapping(pair):
    here = Path(__file__).resolve().parent
    mapping_path = here / Path("list.json")
    with open(mapping_path, "rt", encoding="utf-8") as f:
        pairlist = json.load(f)
    return pairlist[pair]
