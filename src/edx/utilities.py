import xml.etree.ElementTree as ET
import os
import base64
import requests
import logging

def parse_course_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root.attrib['course'], root.attrib['org']

def course_package_path(org,course,workspace_dir):
    # drop package right next to course output
    target_dir = os.path.dirname(workspace_dir)
    tarfile_name = f"{org}-{course}.tar.gz"
    return os.path.join(target_dir, tarfile_name)


def get_api_jwt(client_id,client_secret,endpoint_domain):

    credential = f"{client_id}:{client_secret}"
    encoded_credential = base64.b64encode(credential.encode("utf-8")).decode("utf-8")

    headers = {"Authorization": f"Basic {encoded_credential}", "Cache-Control": "no-cache"}
    data = {"grant_type": "client_credentials", "token_type": "jwt"}

    token_request = requests.post(
        f"{endpoint_domain}/oauth2/access_token", headers=headers, data=data
    )
    logging.debug('got back access token from edx')

    return token_request.json()["access_token"]
