import os
import requests
import uuid
import json
from config import *


def fetch_all_projects():
    URL = 'https://api.todoist.com/sync/v8/sync'
    values = {'token': API_KEY, 'sync_token': '*', 'resource_types': '["projects"]'}
    ## Exception handling / verification of return data can be implemented here
    return exe_post(URL, values)


def create_project(projectname):
    URL = 'https://api.todoist.com/sync/v8/sync'
    argss = {'name': projectname}
    commands = [{'type': 'project_add', 'temp_id': str(uuid.uuid4()), 'uuid': str(uuid.uuid4()), 'args': argss}]  #
    values = {'token': API_KEY, 'sync_token': '*', 'resource_types': '["projects"]', 'commands': commands}
    # print(values)
    ## Exception handling / verification of return data can be implemented here
    return exe_post(URL, values)


def verify_project_created(projectname):
    # There are basically multiple ways to confirm if a project is created, Either trust the API response and check for the result or execute fetch all projects.
    data = fetch_all_projects()
    found = False
    # foundblock = '' #incase if this is required we can return data as well
    for x in data["projects"]:
        if x['name'] == projectname:
            found = True
            # foundblock = x #this is not used for now according to the scope of this interview
            break
    return found


def get_project_id(projectname):
    data = fetch_all_projects()
    projectid = 0
    # foundblock = '' #incase if this is required we can return data as well
    for x in data["projects"]:
        if x['name'] == projectname:
            projectid = x['id']  # this is not used for now according to the scope of this interview
            break
    return projectid


# def create_task(projectid,tasktext):
#    argss = {'content': tasktext,'project_id': projectid}
#    commands = [{'type': 'item_add', 'temp_id': str(uuid.uuid4()), 'uuid': str(uuid.uuid4()), 'args': argss}]  #
#    values = {'token': API_KEY, 'commands': commands}
#    ## Exception handling / verification of return data can be implemented here
#    return exe_post(URL, values)


def get_all_active_items():
    # print(get_project_id("project1"))
    URL = 'https://api.todoist.com/sync/v8/sync'
    values = {'token': API_KEY, 'sync_token': '*', 'resource_types': '["items"]'}
    ## Exception handling / verification of return data can be implemented here
    return exe_post(URL, values)


def get_all_completed_items():
    # print(get_project_id("project1"))
    URL = 'https://api.todoist.com/sync/v8/completed/get_all'
    values = {'token': API_KEY}
    ## Exception handling / verification of return data can be implemented here
    return exe_post(URL, values)


def get_active_item_id(itemname,projectname):
    data = get_all_active_items()
    print(data)
    item_id = 0
    for item in data['items']:
        if str(item['content']) == str(itemname) and str(item["project_id"]) == str(projectname):
            item_id = item['task_id']
            break
    return item_id

def get_completed_item_id(itemname,projectname):
    data = get_all_completed_items()
    print(data)
    item_id = 0
    for item in data['items']:
        if str(item['content']) == str(itemname) and str(item["project_id"]) == str(get_project_id(projectname)):
            item_id = item['task_id']
            break
    return item_id



def reopen_item(itemname,projectname):
    id = get_completed_item_id(itemname,projectname)
    print(id)
    URL = 'https://api.todoist.com/sync/v8/sync'
    argss = {'id': id}
    commands = [{'type': 'item_uncomplete', 'uuid': str(uuid.uuid4()), 'args': argss}]
    values = {'token': API_KEY, 'commands': commands}
    data = exe_post(URL, values)
    print(data)



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
