import os
import requests
import uuid
import json

URL = 'https://api.todoist.com/sync/v8/sync'
API_KEY = '49a99883576f8eb3343859b79e0bdcdab3cf91ac'

def fetch_all_projects():
    values = {'token': API_KEY, 'sync_token': '*', 'resource_types': '["projects"]'}
    ## Exception handling / verification of return data can be implemented here
    return exe_post(URL, values)


def create_project(projectname):
    URL = 'https://api.todoist.com/sync/v8/sync'
    argss = {'name': projectname}
    commands = [{'type' : 'project_add', 'temp_id': str(uuid.uuid4()), 'uuid': str(uuid.uuid4()), 'args': argss}] #
    values = {'token': API_KEY, 'sync_token': '*', 'resource_types': '["projects"]', 'commands': commands}
    #print(values)
    ## Exception handling / verification of return data can be implemented here
    return exe_post(URL, values)




def verify_project_created(projectname):
    #There are basically multiple ways to confirm if a project is created, Either trust the API response and check for the result or execute fetch all projects.
    data = fetch_all_projects()
    found = False
    # foundblock = '' #incase if this is required we can return data as well
    for x in data["projects"]:
        if x['name'] == projectname:
            found = True
            # foundblock = x #this is not used for now according to the scope of this interview
            break
    return found


def exe_post(input_url, input_values):
    data = ''
    try:
        r = requests.post(url=input_url, json=input_values)
        data = r.json()
    except ValueError:
        data = "[{Error}]"
        event_response = "error: %s" % ValueError
        print(event_response)
    return data
