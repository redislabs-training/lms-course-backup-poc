import logging
from pathlib import Path
import mimetypes
from datetime import datetime
import uuid
import markdown
import _hashlib
from dateutil.relativedelta import relativedelta

def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type

def current_datetime():
    # Returns the current date and time in ISO format with a 'Z' suffix
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def future_datetime(months=60):
    current_utc = datetime.utcnow()
    future_utc = current_utc + relativedelta(months=months)
    return future_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

def normalize_short_name(name):
    return name.lower().replace(" ", "-")

def convert_markdown_to_html(markdown_text):
    html = markdown.markdown(markdown_text)
    return html

def full_ref_path(course_path,ref):
    if (ref[0] == "."):
        return f"{course_path}{ref[1:]}"
    else: 
        return ref

def get_hash_id(val:str, len:int = 24):
    val_encoded = val.encode('utf-8')
    return hashlib.sha256(val_encoded).hexdigest()[:len]

def get_id():
    new_uuid = uuid.uuid4()
    return str(new_uuid)

def parse_markdown_sections(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    sections = []
    current_section = {}
    current_content = []

    for line in content:
        if line.startswith('##'):
            if current_section:
                # Finalize the previous section
                current_section['section'] = ''.join(current_content).strip()
                sections.append(current_section)

            # Start a new section
            current_section = {'name': line.strip().lstrip('#').strip()}
            current_content = []
        else:
            # Add line to the current section content
            current_content.append(line)

    # Add the last section
    if current_section:
        current_section['section'] = ''.join(current_content).strip()
        sections.append(current_section)

    return sections