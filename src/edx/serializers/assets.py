
import json
from pathlib import Path
from dataclasses import asdict
from ..config import WORKSPACE

_DIR = f"{WORKSPACE}/policies/"

def add_asset(asset):
    file_path = f"{_DIR}/assets.json"
    if Path(file_path).exists():
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    asset_key = asset.displayname
    data[asset_key] = asdict(asset)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)