import logging
import os
import shutil
import yaml
import xml.etree.ElementTree as ET
import time
from datetime import datetime, timedelta
import hashlib
import random
import string
import html

from .ids import IDs

# globals for now
current_timestamp = int(time.time())

workspace_dir = '/Users/kurtmoeller/Develop/course-backup-poc/moodle-backup-workspace'
course_path = '/Users/kurtmoeller/Develop/course-backup-poc/course-source'
template_dir = '/Users/kurtmoeller/Develop/course-backup-poc/moodle-templates'

ids = IDs()

def random_string(length=20):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def calculate_backupid(ts,tree):
    """Calculate a new backup_id based on Moodle's logic."""
    type_element = tree.find(".//details/detail/type")
    id_element = tree.find(".//contents/course/courseid")
    format_element = tree.find(".//details/detail/format")
    interactive_element = tree.find(".//details/detail/interactive")
    mode_element = tree.find(".//details/detail/mode")

    type_value = type_element.text if type_element is not None else ""
    id_value = id_element.text if id_element is not None else ""
    format_value = format_element.text if format_element is not None else ""
    interactive_value = interactive_element.text if interactive_element is not None else ""
    mode_value = mode_element.text if mode_element is not None else ""

    userid = "1"
    operation = "backup"
    current_time = str(ts)

    backupid_raw = current_time + '-' + type_value + '-' + id_value + '-' + format_value + '-' + \
                   interactive_value + '-' + mode_value + '-' + userid + '-' + operation + '-' + random_string()
    
    logging.info(backupid_raw)

    return hashlib.md5(backupid_raw.encode()).hexdigest()

def convert_learning_objectives_to_markdown(learning_objectives):
    # Convert to Markdown list
    markdown_list = "\n".join([f"- {item}" for item in learning_objectives])

    return markdown_list

def update_xml_element(tree, tag, value):
    for element in tree.iter(tag):
        element.text = value

def create_workspace(workspace_dir, template_dir):
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)
    # Copy the entire contents of the template directory
    shutil.copytree(template_dir, workspace_dir, dirs_exist_ok=True)

def add_element_backup_file(parent_name, child_name, new_element, workspace_dir):
    logging.debug(f"add_element_backup_file - parent_name: {parent_name}, child_name: {child_name}")
    backup_file = os.path.join(workspace_dir, 'moodle_backup.xml')
    tree = ET.parse(backup_file)
    root = tree.getroot()
    parent = root.find(f".//{parent_name}")

    child = ET.Element(child_name)
    for key, value in new_element.items():
        sub = ET.SubElement(child, key)
        sub.text = value
    parent.append(child)
    tree.write(backup_file, encoding='UTF-8', xml_declaration=True)


def update_course_file(course_data):
    update_file = 'course/course.xml'
    # read xml
    tree = ET.parse(os.path.join(workspace_dir, update_file))

    update_xml_element(tree, 'fullname', course_data.get('name', ''))
    update_xml_element(tree, 'shortname', course_data.get('short_name', ''))

    summaryformat_element = tree.find('summaryformat')
    summaryformat_element.text = str(4)
    summary_element = tree.find('summary')
    summary_element.text = f"### {course_data.get('description')}\n\n**Learning Objectives**:\n{convert_learning_objectives_to_markdown(course_data.get('learning_objectives'))}"
    
    #write xml
    tree.write(os.path.join(workspace_dir, update_file), encoding='UTF-8', xml_declaration=True)

def update_moodle_backup_file(course_data):
    update_file = 'moodle_backup.xml'

    # initial vars
    
    filename = course_data.get('name', '').lower().replace(' ', '_') + '.mbz'

    # read xml
    tree = ET.parse(os.path.join(workspace_dir, update_file))

    # update full and short names
    update_xml_element(tree, 'original_course_fullname', course_data.get('name', ''))
    update_xml_element(tree, 'original_course_shortname', course_data.get('short_name', ''))

    short_name_element = tree.find(".//information/contents/course/title")
    short_name_element.text = course_data.get('short_name', '')

    # Update backup_date
    backup_date_element = tree.find(".//backup_date")
    if backup_date_element is not None:
        backup_date_element.text = str(current_timestamp)

    # Update original_course_startdate
    start_date_element = tree.find(".//original_course_startdate")
    if start_date_element is not None:
        start_date_element.text = str(current_timestamp)

    # Update original_course_enddate
    end_date_element = tree.find(".//original_course_enddate")
    if end_date_element is not None:
        end_date_element.text = str(int((datetime.now() + timedelta(days=365 * 10)).timestamp()))

    # Update name in moodle_backup information
    name_element = tree.find(".//information/name")
    if name_element is not None:
        name_element.text = filename

    # Update filename in settings
    for setting in tree.findall(".//settings/setting"):
        if setting.find('name').text == 'filename':
            setting.find('value').text = filename
    
    new_backupid = calculate_backupid(current_timestamp,tree)

    logging.info(new_backupid)

    detail_element = tree.find(".//details/detail")
    if detail_element is not None:
        detail_element.set('backup_id', new_backupid)
    else:
        raise ValueError("The detail element with backup_id attribute was not found in the XML.")
    
    # replace some generic values, not sure it matters
    update_xml_element(tree, 'original_site_identifier_hash', hashlib.md5(random_string().encode()).hexdigest())
    update_xml_element(tree, 'original_course_id', str(random.randint(1, 100)))

    # write xml
    tree.write(os.path.join(workspace_dir, update_file), encoding='UTF-8', xml_declaration=True)


def gen_sections(course_data):
    topics = course_data.get('topics', [])
    num_sections = len(topics)
    sections_dir = f"{workspace_dir}/sections"

    for i in range(num_sections):
        logging.debug(ids.section)
        section_folder = f"section_{ids.section}"
        # Create new section folder
        new_section_folder_full_path = f"{sections_dir}/{section_folder}"
    
        # Copy contents from section_100 to the new folder (it is the general section and there as a template)
        logging.debug(f'{sections_dir}/{section_folder}')
        shutil.copytree(f"{sections_dir}/section_100", new_section_folder_full_path, dirs_exist_ok=True)

        # Update section.xml inside the new folder
        section_tree = ET.parse(f"{new_section_folder_full_path}/section.xml")
        section_root = section_tree.getroot()
        section_root.set('id', str(ids.section))
        #section order
        number_element = section_root.find('number')
        number_element.text = str(ids.section - ids.section_base)

        name_element = section_root.find('name')
        name_element.text = topics[i].get('name')

        summary_element = section_root.find('summary')
        summary_element.text = f"{topics[i].get('descr')}\n\n**Learning Objectives**:\n{convert_learning_objectives_to_markdown(topics[i].get('learning_objectives'))}"

        summaryformat_element = section_root.find('summaryformat')
        summaryformat_element.text = str(4)
        
        # we may want to make this a flag in course descriptor
        visibile_element = section_root.find('visible')
        visibile_element.text = str(1)

        # at this point not sure what it is, but the sections with content have it
        availabilityjson_element = section_root.find('availabilityjson')
        availabilityjson_element.text = '{"op":"&amp;","c":[],"showc":[]}'
        
        modtime_element = section_root.find('timemodified')
        if modtime_element is not None:
            modtime_element.text = str(current_timestamp)


        section_block = {
            'sectionid': str(i),
            'title': topics[i].get('name'),
            'directory': f'sections/{section_folder}'
        }

        add_element_backup_file('information/contents/sections', 'section', section_block, workspace_dir)
        
        setting_included = {
            'level': 'section',
            'section': section_folder,
            'name': f'{section_folder}_included',
            'value': str(1)
        }

        add_element_backup_file('information/settings', 'setting', setting_included, workspace_dir)

        setting_userinfo = {
            'level': 'activity',
            'activity': section_folder,
            'name': f"{section_folder}_userinfo",
            'value': str(0)
        }

        add_element_backup_file('information/settings', 'setting', setting_userinfo, workspace_dir)

        
        content_items = topics[i].get('content_items', [])
        #gen items
        for item in content_items:
            match item.get('type'):
                case 'VIDEO':
                    gen_video(item)
                case 'QUIZ':
                    gen_quiz(item)
                case 'ARTICLE':
                    gen_article(item)
                case 'SLIDES':
                    gen_slides(item)
                case 'LESSON':
                    gen_lesson(item)
                case 'LABEL':
                    gen_label(item)
                case _:
                    logging.error(f"Unknown content type: {item.get('type')}")

            # Find the sequence element
            sequence_element = section_root.find('sequence')

            if sequence_element is not None:
                current_sequence = sequence_element.text

                if current_sequence:
                    # If there's already content, append the new ID with a comma
                    updated_sequence = f"{current_sequence},{ids.module}"
                else:
                    # If the sequence element is empty, just use the new ID
                    updated_sequence = str(ids.module)
                # Update the sequence element
                sequence_element.text = updated_sequence       
        
            ids.incr_module_id
            ids.incr_activity_id
            ids.incr_context_id

        section_tree.write(f"{new_section_folder_full_path}/section.xml", encoding='UTF-8', xml_declaration=True)

        ids.incr_section_id



def gen_video(video_data):

    logging.debug(video_data.get('name'))
    logging.debug(video_data.get('ref'))

    # Copy page template into new activity
    video_folder = f"page_{ids.module}"
    video_activity_path = f"activities/{video_folder}"
    shutil.copytree(f"{workspace_dir}/activities/templates/page", f"{workspace_dir}/{video_activity_path}", dirs_exist_ok=True)

    activity = {
        'moduleid': str(ids.module),
        'sectionid': str(ids.section),
        'modulename': 'page',
        'title': video_data.get('name'),
        'directory': video_activity_path
    }

    add_element_backup_file('information/contents/activities', 'activity', activity, workspace_dir)

    setting_included = {
        'level': 'activity',
        'activity': video_folder,
        'name': f"{video_folder}_included",
        'value': str(1)
    }

    add_element_backup_file('information/settings', 'setting', setting_included, workspace_dir)


    setting_userinfo = {
        'level': 'activity',
        'activity': video_folder,
        'name': f"{video_folder}_userinfo",
        'value': str(0)
    }

    add_element_backup_file('information/settings', 'setting', setting_userinfo, workspace_dir)

    # page.xml
    page_tree = ET.parse(f"{workspace_dir}/{video_activity_path}/page.xml")

    page_tree_root = page_tree.getroot()
    page_tree_root.set('id', str(ids.activity))
    page_tree_root.set('moduleid', str(ids.module))
    page_tree_root.set('contextid', str(ids.context))
    

    page_element = page_tree_root.find('.//page')
    page_element.set('id', str(ids.activity))

    name_element = page_tree_root.find('.//page/name')
    name_element.text = video_data.get('name')
    
    # Read the content from the external file
    # Determine the file type and set contentformat accordingly
    if video_data.get('ref').startswith('.'):
        ref = f"{course_path}/{video_data.get('ref')[2:]}" 
    elif video_data.get('ref').startswith('.md'):
        ref = video_data.get('ref')
    else:
        raise ValueError("Unsupported start for VIDEO ref")
    
    with open(ref, 'r', encoding='utf-8') as file:
        content = file.read()

    # Encode the content for XML
    encoded_content = html.escape(content)

    content_element = page_tree_root.find('.//page/content')
    content_element.text = str(encoded_content)

    # Determine the file type and set contentformat accordingly
    if video_data.get('ref').endswith('.html'):
        contentformat = '1'  # HTML
    elif video_data.get('ref').endswith('.md'):
        contentformat = '4'  # Markdown
    else:
        raise ValueError("Unsupported file type")
    
    contentformat_element = page_tree_root.find('.//page/contentformat')
    contentformat_element.text = str(contentformat)

    display_element = page_tree_root.find('.//page/display')
    if display_element is not None:
        display_element.text = str(5)

    modtime_element = page_tree_root.find('.//page/timemodified')
    if modtime_element is not None:
        modtime_element.text = str(current_timestamp)

    page_tree.write(f"{workspace_dir}/{video_activity_path}/page.xml", encoding='UTF-8', xml_declaration=True)

    # module.xml
    module_tree = ET.parse(f"{workspace_dir}/{video_activity_path}/module.xml")

    module_tree_root = module_tree.getroot()
    module_tree_root.set('id', str(ids.module))

    sectionid_element = module_tree_root.find('sectionid')
    if sectionid_element is not None:
        sectionid_element.text = str(ids.section)

    sectionnumber_element = module_tree_root.find('sectionnumber')
    if sectionnumber_element is not None:
        sectionnumber_element.text = str(ids.section-ids.section_base)
    

    addedtime_element = module_tree_root.find('added')
    if addedtime_element is not None:
        addedtime_element.text = str(current_timestamp)

    module_tree.write(f"{workspace_dir}/{video_activity_path}/module.xml", encoding='UTF-8', xml_declaration=True)

def gen_quiz(quiz_data):
    logging.info(quiz_data.get('name'))

def gen_article(article_data):
    logging.info(article_data.get('name'))

def gen_slides(slides_data):
    logging.info(slides_data.get('name'))

def gen_lesson(lesson_data):
    logging.info(lesson_data.get('name'))

def gen_label(label_data):
    logging.info(label_data.get('name'))


def main():

    logging.basicConfig(level=logging.DEBUG)

    create_workspace(workspace_dir,template_dir)

    # Load the course.yaml file
    with open(f'{course_path}/course.yaml', 'r') as file:
        course_data = yaml.safe_load(file)

    update_course_file(course_data)
    update_moodle_backup_file(course_data)
    gen_sections(course_data)





if __name__ == '__main__':
    main()