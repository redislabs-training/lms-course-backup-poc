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

def update_course_file(update_file, course_data, workspace_dir):

    # read xml
    tree = ET.parse(os.path.join(workspace_dir, update_file))

    update_xml_element(tree, 'fullname', course_data.get('name', ''))
    update_xml_element(tree, 'shortname', course_data.get('short_name', ''))

    summaryformat_element = tree.find('summaryformat')
    if summaryformat_element is not None:
        summaryformat_element.text = str(4)
    summary_element = tree.find('summary')
    if summary_element is not None:
        summary_element.text = f"### {course_data.get('description')}\n\n**Learning Objectives**:\n{convert_learning_objectives_to_markdown(course_data.get('learning_objectives'))}"
    
    #write xml
    tree.write(os.path.join(workspace_dir, update_file), encoding='UTF-8', xml_declaration=True)

def update_moodle_backup_file(update_file, course_data, workspace_dir):

    # initial vars
    current_timestamp = int(time.time())
    filename = course_data.get('name', '').lower().replace(' ', '_') + '.mbz'

    # read xml
    tree = ET.parse(os.path.join(workspace_dir, update_file))

    # update full and short names
    update_xml_element(tree, 'original_course_fullname', course_data.get('name', ''))
    update_xml_element(tree, 'original_course_shortname', course_data.get('short_name', ''))

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


def generate_sections(update_file, course_data, workspace_dir):
    topics = course_data.get('topics', [])
    num_sections = len(topics)
    sections_dir = f"{workspace_dir}/sections"

    # read xml
    tree = ET.parse(os.path.join(workspace_dir, update_file))

    settings = tree.find('.//settings')

    # Start from section ID 100
    section_id = 101

    for i in range(num_sections):
        # Create new section folder
        new_section_folder = f"{sections_dir}/section_{section_id}"
        #if not os.path.exists(new_section_folder):
        #os.makedirs(new_section_folder)
    
        # Copy contents from section_100 to the new folder (it is the general section and there as a template)
        shutil.copytree(f"{sections_dir}/section_100", new_section_folder, dirs_exist_ok=True)

        # Update section.xml inside the new folder
        section_tree = ET.parse(f"{new_section_folder}/section.xml")
        section_root = section_tree.getroot()
        section_root.set('id', str(section_id))
        name_element = section_root.find('name')
        if name_element is not None:
            name_element.text = topics[i].get('name')
        modtime_element = section_root.find('timemodified')
        if modtime_element is not None:
            modtime_element.text = str(int(time.time()))
        summaryformat_element = section_root.find('summaryformat')
        if summaryformat_element is not None:
            summaryformat_element.text = str(4)
        summary_element = section_root.find('summary')
        if summary_element is not None:
            summary_element.text = f"{topics[i].get('descr')}\n\n**Learning Objectives**:\n{convert_learning_objectives_to_markdown(topics[i].get('learning_objectives'))}"
        section_tree.write(f"{new_section_folder}/section.xml", encoding='UTF-8', xml_declaration=True)

        # Add new setting blocks in moodle_backup.xml
        for setting_name in ['included', 'userinfo']:
            setting_element = ET.SubElement(settings, 'setting')
            ET.SubElement(setting_element, 'level').text = 'section'
            ET.SubElement(setting_element, 'section').text = f'section_{section_id}'
            ET.SubElement(setting_element, 'name').text = f'section_{section_id}_{setting_name}'
            ET.SubElement(setting_element, 'value').text = '1' if setting_name == 'included' else '0'

        # Increment section_id for next iteration
        section_id += 1

    # Save the updated moodle_backup.xml
    tree.write(os.path.join(workspace_dir, update_file), encoding='UTF-8', xml_declaration=True)



def main():

    logging.basicConfig(level=logging.DEBUG)

    workspace_dir = '/Users/kurtmoeller/Develop/course-backup-poc/moodle-backup-workspace'  # Set your default values
    course_yaml_path = '/Users/kurtmoeller/Develop/course-backup-poc/course-source/course.yaml'   # Set your default values
    template_dir = '/Users/kurtmoeller/Develop/course-backup-poc/moodle-templates'          # Set your default values

    create_workspace(workspace_dir,template_dir)

    # Load the course.yaml file
    with open(course_yaml_path, 'r') as file:
        course_data = yaml.safe_load(file)

    update_course_file('course/course.xml', course_data, workspace_dir)
    update_moodle_backup_file('moodle_backup.xml', course_data, workspace_dir)
    generate_sections('moodle_backup.xml', course_data, workspace_dir)





if __name__ == '__main__':
    main()