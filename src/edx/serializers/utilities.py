import mimetypes
import json
from datetime import datetime
from dataclasses import asdict
from pathlib import Path
from ..config import WORKSPACE

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type

def current_datetime():
    # Returns the current date and time in ISO format with a 'Z' suffix
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def add_asset(asset):
    file_path = f"{WORKSPACE}/policies/assets.json"
    if Path(file_path).exists():
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    asset_key = asset.displayname
    data[asset_key] = asdict(asset)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def normalize_short_name(name):
    return name.lower().replace(" ", "-")