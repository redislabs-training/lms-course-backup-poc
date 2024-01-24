import os
import logging
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import html
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
                _add_quiz(item,sequential_id)
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
    slide_elem.set("xblock-family", "xblock.v1")

    add_elem_vertical(vertical_id, slide_elem)

    # add to asset.json
    son = ContentSon(name=asset_filename,course=name,org=ORG)
    asset_obj = {'contentType':get_mime_type(item.ref),
        'displayname': asset_filename,
        'filename': f'asset-v1:edu+{course.version}+{name}+type@asset+block@{asset_filename}',
        'content_son': son,
        'thumbnail_location': None
        }
    asset = Asset(**asset_obj)
    add_asset(asset)

def _add_html(vertical_id,name, html):
    html_id = get_id()
    html_file_name = f"{WORKSPACE}/html/{html_id}.html"
    html_file = open(html_file_name, 'w')
    html_file.writelines(html)

    file_path = f"{WORKSPACE}/html/{html_id}.xml"
    html_elem = ET.Element("html",file_name=html_id, display_name=name, editor="raw")
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

    steps = parse_markdown_sections(source_file,'##')
    logging.debug(steps)

    for step in steps:
        html = convert_markdown_to_html(step['section'])

        _add_html(vertical_id, step['name'], html)

def _create_multi_choice_problem(label, choices):
    parts = choices.strip().split("\n>")
    choice_text = parts[0].strip()
    explanation = parts[1].strip() if len(parts) > 1 else ""

    markdown_representation = f'>>{html.escape(label)}<<\n{html.escape(choice_text)}'
    if explanation:
        markdown_representation += f'\n\n[explanation]{html.escape(explanation)}[explanation]'
    problem = ET.Element("problem", display_name="Multiple Choice", markdown=markdown_representation)
    c_response = ET.SubElement(problem, "choiceresponse")
    ET.SubElement(c_response, "label").text = label
    checkbox_group = ET.SubElement(c_response, "checkboxgroup")
    for choice_line in choice_text.split('\n'):
        if choice_line.strip():
            correct = "true" if "[x]" in choice_line else "false"
            choice_text = choice_line.replace("[x]", "").replace("[ ]", "").strip()
            choice_elem = ET.SubElement(checkbox_group, "choice", correct=correct)
            choice_elem.text = choice_text

    if explanation:
        solution = ET.SubElement(c_response, "solution")
        detailed_solution = ET.SubElement(solution, "div", {"class": "detailed-solution"})
        ET.SubElement(detailed_solution, "p").text = "Explanation"
        ET.SubElement(detailed_solution, "p").text = explanation
    
    return problem

def _create_single_choice_problem(label, choices):
    parts = choices.strip().split("\n>")
    choice_text = parts[0].strip()
    explanation = parts[1].strip() if len(parts) > 1 else ""

    markdown_representation = f'>>{html.escape(label)}<<\n{html.escape(choice_text)}'
    if explanation:
        markdown_representation += f'\n\n[explanation]{html.escape(explanation)}[explanation]'
    problem = ET.Element("problem", display_name="Multiple Choice", markdown=markdown_representation)
    mc_response = ET.SubElement(problem, "multiplechoiceresponse")
    ET.SubElement(mc_response, "label").text = label
    choice_group = ET.SubElement(mc_response, "choicegroup", type="MultipleChoice")
    for choice_line in choice_text.split('\n'):
        if choice_line.strip():
            correct = "true" if "[x]" in choice_line else "false"
            choice_text = choice_line.replace("[x]", "").replace("[ ]", "").strip()
            choice_elem = ET.SubElement(choice_group, "choice", correct=correct)
            choice_elem.text = choice_text

    if explanation:
        solution = ET.SubElement(mc_response, "solution")
        detailed_solution = ET.SubElement(solution, "div", {"class": "detailed-solution"})
        ET.SubElement(detailed_solution, "p").text = "Explanation"
        ET.SubElement(detailed_solution, "p").text = explanation
    
    return problem

def _create_string_response_problem(label, answer):
    markdown_representation = f">>{html.escape(label)}<<\n\n= {html.escape(answer.replace('- ','= ',1))}\n"
    problem = ET.Element("problem", display_name="Text Input", markdown=markdown_representation)
    string_response = ET.SubElement(problem, "stringresponse", answer=answer.replace('- ','',1), type="ci")
    ET.SubElement(string_response, "label").text = label
    ET.SubElement(string_response, "textline", size="20")
    
    return problem

def _add_problem(vertical_id,problem):
    problem_id = get_id()
    file_path = f"{WORKSPACE}/problem/{problem_id}.xml"
    tree = ET.ElementTree(problem)
    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'Added new problem at {file_path}')

    problem_vertical_elem = ET.Element("problem", url_name=problem_id)
    add_elem_vertical(vertical_id, problem_vertical_elem)

def _add_quiz(item,sequential_id):
    vertical_id = get_id()
    gen_vertical(vertical_id, item.name)
    add_vertical_sequential(sequential_id, vertical_id)

    source_file = full_ref_path(COURSE_SOURCE, item.ref)

    sections = parse_markdown_sections(source_file, '##')

    for section in sections:
        label = section['name']
        choices = section['section']

        correct_answers = choices.count('[x]')

        if correct_answers == 1:
            problem = _create_single_choice_problem(label,choices)
            _add_problem(vertical_id,problem)
        elif correct_answers > 1:
            problem = _create_multi_choice_problem(label,choices)
            _add_problem(vertical_id,problem)
        elif '__' in label:
            problem = _create_string_response_problem(label,choices)
            _add_problem(vertical_id,problem)
        else:
            logging.error('cannot detect problem type')
        
        