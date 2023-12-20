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

from .IDs import IDs
from .Lesson import LVals, LPage, LAnswer

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

def add_element_to_file(parent_name, child_name, new_element, file_path):
    logging.debug(f"add_element_to_file - parent_name: {parent_name}, child_name: {child_name}")
    file = os.path.join(workspace_dir, file_path)
    tree = ET.parse(file)
    root = tree.getroot()
    parent = root.find(f".//{parent_name}")

    child = ET.Element(child_name)
    for key, value in new_element.items():
        sub = ET.SubElement(child, key)
        sub.text = value
    parent.append(child)
    tree.write(file, encoding='UTF-8', xml_declaration=True)


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

        add_element_to_file('information/contents/sections', 'section', section_block, 'moodle_backup.xml')
        
        setting_included = {
            'level': 'section',
            'section': section_folder,
            'name': f'{section_folder}_included',
            'value': str(1)
        }

        add_element_to_file('information/settings', 'setting', setting_included, 'moodle_backup.xml')

        setting_userinfo = {
            'level': 'activity',
            'activity': section_folder,
            'name': f"{section_folder}_userinfo",
            'value': str(0)
        }

        add_element_to_file('information/settings', 'setting', setting_userinfo, 'moodle_backup.xml')

        
        content_items = topics[i].get('content_items', [])
        #gen items
        for item in content_items:
            match item.get('type'):
                case 'VIDEO':
                    gen_page(item)
                case 'QUIZ':
                    gen_quiz(item)
                case 'ARTICLE':
                    gen_page(item)
                case 'SLIDES':
                    gen_resource(item)
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
        
            ids.incr_module()
            logging.debug(f'module id:{ids.module}')
            ids.incr_activity()
            ids.incr_context()

        section_tree.write(f"{new_section_folder_full_path}/section.xml", encoding='UTF-8', xml_declaration=True)

        ids.incr_section()

def gen_activity_general(type, name, activity_folder, activity_path):

    shutil.copytree(f"{workspace_dir}/activities/templates/general", f"{workspace_dir}/{activity_path}", dirs_exist_ok=True)

    shutil.copy(f"{workspace_dir}/activities/templates/{type}.xml", f"{workspace_dir}/{activity_path}/")

    activity = {
        'moduleid': str(ids.module),
        'sectionid': str(ids.section),
        'modulename': 'page',
        'title': name,
        'directory': activity_path
    }

    add_element_to_file('information/contents/activities', 'activity', activity, 'moodle_backup.xml')

    setting_included = {
        'level': 'activity',
        'activity': activity_folder,
        'name': f"{activity_folder}_included",
        'value': str(1)
    }

    add_element_to_file('information/settings', 'setting', setting_included, 'moodle_backup.xml')


    setting_userinfo = {
        'level': 'activity',
        'activity': activity_folder,
        'name': f"{activity_folder}_userinfo",
        'value': str(0)
    }

    add_element_to_file('information/settings', 'setting', setting_userinfo, 'moodle_backup.xml')

   # basic updates to the main activity file
    tree = ET.parse(f"{workspace_dir}/{activity_path}/{type}.xml")

    tree_root = tree.getroot()
    tree_root.set('id', str(ids.activity))
    tree_root.set('moduleid', str(ids.module))
    tree_root.set('contextid', str(ids.context))
    

    main_element = tree_root.find(f'.//{type}')
    main_element.set('id', str(ids.activity))

    name_element = tree_root.find(f'.//{type}/name')
    name_element.text = name

    tree.write(f"{workspace_dir}/{activity_path}/{type}.xml", encoding='UTF-8', xml_declaration=True)

    # module.xml
    module_tree = ET.parse(f"{workspace_dir}/{activity_path}/module.xml")

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

    module_tree.write(f"{workspace_dir}/{activity_path}/module.xml", encoding='UTF-8', xml_declaration=True)
    
def gen_page(activity_data):
    
    logging.debug(activity_data.get('name'))
    logging.debug(activity_data.get('ref'))


    # Copy page template into new activity
    type = 'page'
    activity_folder = f"{type}_{ids.module}"
    activity_path = f"activities/{activity_folder}"

    gen_activity_general(type, activity_data.get('name'), activity_folder, activity_path)

    # page.xml
    page_tree = ET.parse(f"{workspace_dir}/{activity_path}/{type}.xml")

    page_tree_root = page_tree.getroot()
    
    # Read the content from the external file
    # Determine the file type and set contentformat accordingly
    if activity_data.get('ref').startswith('.'):
        ref = f"{course_path}/{activity_data.get('ref')[2:]}" 
    elif activity_data.get('ref').startswith('.md'):
        ref = activity_data.get('ref')
    else:
        raise ValueError("Unsupported start for activity ref")
    
    with open(ref, 'r', encoding='utf-8') as file:
        content = file.read()

    # Encode the content for XML
    encoded_content = html.escape(content)

    content_element = page_tree_root.find('.//page/content')
    content_element.text = str(encoded_content)

    # Determine the file type and set contentformat accordingly
    if activity_data.get('ref').endswith('.html'):
        contentformat = '1'  # HTML
    elif activity_data.get('ref').endswith('.md'):
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

    page_tree.write(f"{workspace_dir}/{activity_path}/page.xml", encoding='UTF-8', xml_declaration=True)

def gen_lesson(activity_data):
    logging.debug(activity_data.get('name'))
    logging.debug(activity_data.get('ref'))

    # Copy page template into new activity
    type = 'lesson'
    activity_folder = f"{type}_{ids.module}"
    activity_path = f"activities/{activity_folder}"

    gen_activity_general(type, activity_data.get('name'), activity_folder, activity_path)

    # lesson.xml
    lesson_tree = ET.parse(f"{workspace_dir}/{activity_path}/{type}.xml")
    lesson_tree_root = lesson_tree.getroot()
    lesson_vals = LVals()

    name_element = lesson_tree_root.find('.//lesson/name')
    name_element.text = activity_data.get('name')

    course_element = lesson_tree_root.find('.//lesson/course')
    course_element.text = str(ids.course)

    modified_element = lesson_tree_root.find('.//lesson/timemodified')
    modified_element.text = activity_data.get(current_timestamp)

    lesson_tree.write(f"{workspace_dir}/{activity_path}/lesson.xml", encoding='UTF-8', xml_declaration=True)
    
    # Read the content from the external file
    ref = f"{course_path}/{activity_data.get('ref')[2:]}"
    with open(ref, 'r', encoding='utf-8') as file:
        markdown_text = file.read()
    
    sections = markdown_text.split('##')[1:]  # Split by '##' and skip the first chunk if it's before the first '##'

    num_sections = len(sections)

    pages = []

    for i, section in enumerate(sections):
        lines = section.strip().split('\n', 1)
        heading = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ''

        if i == 0:
            beg_answer = LAnswer(id=str(ids.lesson_answer),
                                 jumpto=lesson_vals.next_jumpto,
                                 timecreated=str(current_timestamp),
                                 answer_text=lesson_vals.next_text)
            ids.incr_lesson_answer()
            pages.append(LPage(id=ids.lesson_page,
                         nextpageid=str(ids.lesson_page+1),
                         timecreated=current_timestamp,
                         title=heading,contents=content,
                         answers=[beg_answer]))
        elif i == num_sections - 1:
            mid1_answer = LAnswer(id=str(ids.lesson_answer),
                                  jumpto=lesson_vals.previous_jumpto,
                                  timecreated=str(current_timestamp),
                                  answer_text=lesson_vals.previous_text)
            ids.incr_lesson_answer()
            mid2_answer = LAnswer(id=ids.lesson_answer,
                                  jumpto=lesson_vals.next_jumpto,
                                  timecreated=str(current_timestamp),
                                  answer_text=lesson_vals.next_text)
            ids.incr_lesson_answer()
            pages.append(LPage(id=ids.lesson_page,
                         previouspageid=str(ids.lesson_page-1),
                         nextpageid=str(ids.lesson_page+1),
                         timecreated=str(current_timestamp),
                         title=heading,contents=content,
                         answers=[mid1_answer,mid2_answer]))
        else: 
            mid1_answer = LAnswer(id=ids.lesson_answer, 
                                  jumpto=lesson_vals.previous_jumpto, 
                                  timecreated=current_timestamp, 
                                  answer_text=lesson_vals.previous_text)
            ids.incr_lesson_answer()
            end_answer = LAnswer(id=ids.lesson_answer, 
                                 jumpto=lesson_vals.end_jumpto, 
                                 timecreated=current_timestamp, 
                                 answer_text=lesson_vals.end_text)
            ids.incr_lesson_answer()
            pages.append(LPage(id=ids.lesson_page,
                         previouspageid=str(ids.lesson_page-1),
                         timecreated=current_timestamp,
                         title=heading,contents=content,
                         answers=[mid1_answer,end_answer]))
        ids.incr_lesson_page()

    for page in pages:
        print(page.__dict__) 

 

def gen_quiz(activity_data):
    logging.debug(activity_data.get('name'))
    logging.debug(activity_data.get('ref'))

    # Copy page template into new activity
    type = 'quiz'
    activity_folder = f"{type}_{ids.module}"
    activity_path = f"activities/{activity_folder}"

    gen_activity_general(type, activity_data.get('name'), activity_folder, activity_path)

def gen_resource(activity_data):
    logging.debug(activity_data.get('name'))
    logging.debug(activity_data.get('ref'))

    # Copy page template into new activity
    type = 'resource'
    activity_folder = f"{type}_{ids.module}"
    activity_path = f"activities/{activity_folder}"

    gen_activity_general(type, activity_data.get('name'), activity_folder, activity_path)


def gen_label(activity_data):
    logging.debug(activity_data.get('name'))
    logging.debug(activity_data.get('ref'))

    # # Copy page template into new activity
    # type = 'label'
    # activity_folder = f"{type}_{ids.module}"
    # activity_path = f"activities/{activity_folder}"

    # gen_activity_general(type, activity_data.get('name'), activity_folder, activity_path)

def remove_templates():
    shutil.rmtree(f'{workspace_dir}/activities/templates')

def main():

    logging.basicConfig(level=logging.DEBUG)

    create_workspace(workspace_dir,template_dir)

    # Load the course.yaml file
    with open(f'{course_path}/course.yaml', 'r') as file:
        course_data = yaml.safe_load(file)

    update_course_file(course_data)
    update_moodle_backup_file(course_data)
    gen_sections(course_data)
    remove_templates()





if __name__ == '__main__':
    main()