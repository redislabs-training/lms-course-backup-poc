import os
import logging
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
from ..config import COURSE_SOURCE, WORKSPACE, ORG
from .utilities import normalize_short_name, get_mime_type, get_id, convert_markdown_to_html, full_ref_path, parse_markdown_sections
from .assets import add_asset
from src.course_entities import ContentItemType
from .entities import ContentSon, Asset
from .sequential import add_vertical_sequential

_DIR = f"{WORKSPACE}/vertical"

def gen_verticals(sequential_id,content_items,course):
    logging.info(f"creating content items for sequential: {sequential_id}")
    for item in content_items:
        logging.debug(item)
        match item.type:
            case ContentItemType.SLIDES:
                logging.debug('SLIDES')
                _add_slide(item,sequential_id,course)
            case ContentItemType.VIDEO:
                logging.debug('VIDEO')
                _add_video(item,sequential_id)
            case ContentItemType.ARTICLE:
                logging.debug('ARTICLE')
                _add_article(item,sequential_id)
            case ContentItemType.QUIZ:
                logging.debug('QUIZ')
            case ContentItemType.EXERCISE:
                logging.debug('EXERCISE')
                _add_exercise(item,sequential_id)


def gen_vertical(vertical_id,name):
    file_path = os.path.join(_DIR, f"{vertical_id}.xml")
    chapter_elem = ET.Element("vertical", display_name=name)
    tree = ET.ElementTree(chapter_elem)
    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'write new vertical at {file_path}')

def add_elem_vertical(vertical_id, vertical_elem):
    file_path = os.path.join(_DIR, f"{vertical_id}.xml")
    tree = ET.parse(file_path)
    root = tree.getroot()
    if root.tag != 'vertical':
        logging.error(f"The root element of {file_path} is not 'vertical'.")
        return
    root.append(vertical_elem)

    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'Appended new element to vertical at {file_path}')


def _add_slide(item,sequential_id,course):
    vertical_id = get_id()
    pdf_id = get_id()
    gen_vertical(vertical_id, item.name)
    asset_filename = item.name.replace(" ","")
    shutil.copy(f'{COURSE_SOURCE}/{item.ref}', f'{WORKSPACE}/static/{asset_filename}.pdf')
    name = normalize_short_name(course.short_name)

    ## add vertical to sequence
    add_vertical_sequential(sequential_id,vertical_id)
    
    slide_elem = ET.Element("pdf",
                            url_name=pdf_id,
                            display_name=item.name,
                            href=f"/static/{asset_filename}"
                            )
    slide_elem.set("xblock-family", "xbock.v1")

    add_elem_vertical(vertical_id, slide_elem)

    # add to asset.json
    son = ContentSon(name=asset_filename,course=name,org=ORG)
    asset_obj = {'contentType':get_mime_type(item.ref),
        'displayname': asset_filename,
        'filename': f'asset-v1:edu+{course.version}+{name}+type@asset+block@{asset_filename}',
        'content_son': son,
        'thumbnail_location': ["c4x","edu",course.version,"thumbnail",asset_filename,None]
        }
    asset = Asset(**asset_obj)
    add_asset(asset)

def _add_html(vertical_id,name, html):
    html_id = get_id()
    html_file_name = f"{WORKSPACE}/html/{html_id}.html"
    html_file = open(html_file_name, 'w')
    html_file.writelines(html)

    file_path = f"{WORKSPACE}/html/{html_id}.xml"
    html_elem = ET.Element("html", display_name=name, editor="raw")
    tree = ET.ElementTree(html_elem)
    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'write new vertical at {file_path}')
    
    html_vertical_elem = ET.Element("html", url_name=html_id)

    add_elem_vertical(vertical_id, html_vertical_elem)

def _add_article(item,sequential_id):
    vertical_id = get_id()
    gen_vertical(vertical_id, item.name)
    ## add vertical to sequence
    add_vertical_sequential(sequential_id,vertical_id)

    source_file = full_ref_path(COURSE_SOURCE,item.ref)

    logging.debug(f"source_file: {source_file}")
    if source_file.endswith('.md'): 
        markdown = Path(source_file).read_text()
        html = convert_markdown_to_html(markdown)
    elif source_file.endswith('.html'): 
        html = Path(source_file).read_text()
    else:
        logging.error(f"file is not a supported article type")
        return
    _add_html(vertical_id, item.name, html)

def _add_video(item,sequential_id):
    vertical_id = get_id()
    gen_vertical(vertical_id, item.name)
    ## add vertical to sequence
    add_vertical_sequential(sequential_id,vertical_id)
    html = Path(full_ref_path(COURSE_SOURCE,item.ref)).read_text()
    _add_html(vertical_id, item.name, html)

def _add_exercise(item,sequential_id):
    vertical_id = get_id()
    gen_vertical(vertical_id, item.name)
    add_vertical_sequential(sequential_id,vertical_id)

    source_file = full_ref_path(COURSE_SOURCE,item.ref)

    steps = parse_markdown_sections(source_file)
    logging.debug(steps)

    for step in steps:
        html = convert_markdown_to_html(step['section'])

        _add_html(vertical_id, step['name'], html)