from influxdb_client import InfluxDBClient
from subprocess import Popen, PIPE

from urllib3.exceptions import LocationValueError, NewConnectionError
from influxdb_client.rest import ApiException

import os
import requests

def get_resources():
    '''    '''
    far_flux_dir = f'C:/Users/{os.getlogin()}/AppData/Local/Programs/FarFlux/'
    url = "https://raw.githubusercontent.com/HB9VQQ/FarFlux/main/"

    if not os.path.exists(far_flux_dir):
        os.mkdir(far_flux_dir)
    os.chdir(far_flux_dir)
    
    if not os.path.exists('geohash.json'):
        fname = "geohash.json"
        r = requests.get(url+fname)
        open(fname, "wb").write(r.content)

    if not os.path.exists("radio_tower.ico"):
        fname = "radio_tower.ico"
        r = requests.get(url+fname)
        open(fname, "wb").write(r.content)
    
    if not os.path.exists("radio_tower.png"):
        fname = "radio_tower.png"
        r = requests.get(url+fname)
        open(fname, "wb").write(r.content)

def connection_test(url, token, org_id, bucket):
    '''
    status codes:
    0 --> No host specified
    1 --> Succesful
    2 --> OrganizationID incorrectly configured
    3 --> Bucket incorrectly configured
    4 --> OrgID & Bucket incorrectly configured
    '''
    client = InfluxDBClient(url=url,
                            token=token)
    try:
        organizations = client.organizations_api().find_organizations()
        buckets = client.buckets_api().find_buckets()
    except ApiException:
        status = 0
        message = 'Connection to host not authorized.\n\nCheck token permissions or protocol.'
        return (status, message)
    except LocationValueError:
        status = 0
        message = 'Couldn\'t establish connection to host.\n\nCheck InfluxDB URL.'
        return (status, message)
    except NewConnectionError:
        status = 0
        message = 'Couldn\'t establish connection to host.\n\nCheck InfluxDB URL or network connection.'
        return (status, message)
    bucket_names = []
    for b in buckets.buckets:
        bucket_names.append(b.name)
    org_names = []
    org_ids = []
    for o in organizations:
        org_names.append(o.name)
        org_ids.append(o.id)
    bucket_ok = True if bucket in bucket_names else False
    if org_id in org_names or org_id in org_ids:
        org_ok = True 
    else:
        org_ok = False
    if bucket_ok and org_ok:
        status = 1
        message = 'Successful'
    elif bucket_ok == True and org_ok == False:
        status = 2
        message = f'Organization not found!\n\nAvailable organizations:\n\tOrgID: {org_ids}\n\tOrgName: {org_names}'
    elif bucket_ok == False and org_ok == True:
        status = 3
        message = f'Bucket not found!\n\nAvailable Buckets:\n\t{bucket_names}'
    else:
        status = 4
        message = f'Organization & bucket not found!\n\nAvailable organizations:\n\tOrgID: {org_ids}\n\tOrgName: {org_names}\n\nAvailable buckets:\n\t{bucket_names}'
    return (status, message)

def get_tasks():
    '''
    returns all scheduled tasks on user's system
    schema: {'TaskName': {'NextRunTime': NextRunTime, 'Status': Status}
    '''
    proc = Popen('schtasks /query /fo CSV /nh', stdout=PIPE, shell=True)
    output = proc.stdout.read()
    proc.stdout.close()
    lines = output.splitlines()
    tasks = {}
    item = 1
    for line in lines:
        try:
            value_list = line.decode(encoding="utf-8").split(',')
        except UnicodeDecodeError:
            continue
        tasks[value_list[0].replace('\"', '')] = {
            "NextRunTime": value_list[1].replace('\"', ''),
            "Status": value_list[2].replace('\"', '')
            }
        item += 1
    return tasks

def ch_task_status(status):
    '''
    /ENABLE | /DISABLE
    '''
    task_name = '\FarFlux_Upload'
    command = f'schtasks /change /tn {task_name} status'
    proc = Popen(command, stdout=PIPE, shell=True)
    output = proc.stdout.read()
    proc.stdout.close()
    return output

def delete_task():
    '''    '''
    task_name = '\FarFlux_Upload'
    command = f'schtasks /delete /tn {task_name} /f'
    proc = Popen(command, stdout=PIPE, shell=True)
    output = proc.stdout.read()
    proc.stdout.close()
    return output

def check_task():
    '''    '''
    tasks = get_tasks()
    existing_task = '\FarFlux_Upload' in tasks.keys()
    result = 0
    message = 'FarFlux upload task not scheduled.'
    if existing_task:
        result = 1
        next_run = tasks["\FarFlux_Upload"]["NextRunTime"] 
        task_status = tasks["\FarFlux_Upload"]["Status"]
        message = f'FarFlux upload scheduled.\nNext run: {next_run}\nStatus: {task_status}'
    return (message, result)

def create_task():
    '''    '''
    check = check_task()
    if check[1] != 0:
        return check[0]
    task_name = 'FarFlux_Upload'
    interval = 15
    task_command = f'"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\FarFlux\\FarFlux_upload.exe"'
    proc = Popen(f'schtasks /create /sc minute /mo {interval} /tn {task_name} /tr {task_command}',
                 stdout=PIPE, shell=True)
    output = proc.stdout.read()
    proc.stdout.close()
    msg = output # unused
    tasks = get_tasks()
    next_run = tasks["\FarFlux_Upload"]["NextRunTime"]
    task_status = tasks["\FarFlux_Upload"]["Status"]
    message = f'FarFlux upload task created.\nNext run: {next_run}\nStatus: {task_status}'
    return message
