from influxdb_client import InfluxDBClient
from subprocess import Popen, PIPE

from urllib3.exceptions import LocationValueError, NewConnectionError
from influxdb_client.rest import ApiException

import os
import wget

def get_resources():
    '''    '''
    far_flux_dir = f'C:/Users/{os.getlogin()}/AppData/Roaming/FarFlux/'
    if not os.path.exists(far_flux_dir):
        os.mkdir(far_flux_dir)
    os.chdir(far_flux_dir)
    if not os.path.exists('geohash.json'):
        wget.download('https://raw.githubusercontent.com/HB9VQQ/FarFlux/main/geohash.json')
    if not os.path.exists("radio_tower.ico"):
        wget.download('https://raw.githubusercontent.com/HB9VQQ/FarFlux/main/radio_tower.ico')
    if not os.path.exists("radio_tower.png"):
        wget.download('https://raw.githubusercontent.com/HB9VQQ/FarFlux/main/radio_tower.png')

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
    proc = Popen('schtasks /query /fo CSV', stdout=PIPE)
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
        if value_list[0].replace('\"', '') == "TaskName":
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
    command = ['schtasks', '/change', '/tn', task_name, status]
    proc = Popen(command, stdout=PIPE)
    output = proc.stdout.read()
    proc.stdout.close()
    return output.decode("utf-8")

def delete_task():
    '''    '''
    task_name = '\FarFlux_Upload'
    command = ['schtasks', '/delete', '/tn', task_name, '/f']
    proc = Popen(command, stdout=PIPE)
    output = proc.stdout.read()
    proc.stdout.close()
    return output.decode("utf-8")

def check_task(take_action):
    '''    '''
    tasks = get_tasks()
    existing_task = '\FarFlux_Upload' in tasks.keys()
    result = 0
    message = 'FarFlux upload task not scheduled.'
    if existing_task:
        next_run = tasks["\FarFlux_Upload"]["NextRunTime"] 
        task_status = tasks["\FarFlux_Upload"]["Status"]
        if task_status == 'Ready':
            result = 1
            message = f'FarFlux upload task scheduled.\nNext run: {next_run}'
        elif task_status == 'Disabled':
            if take_action == True:
                msg = ch_task_status('/ENABLE')
                tasks = get_tasks()
                next_run = tasks["\FarFlux_Upload"]["NextRunTime"]
                if 'SUCCESS' in msg:
                    result = 2
                    message = f'FarFlux upload task enabled.\nNext run: {next_run}'
                else:
                    result = 3
                    message = msg
            else:
                result = 9
                message = f'FarFlux upload status: {task_status}'
        else:
            if take_action == True:
                msg = delete_task()
                if 'SUCCESS' in msg:
                    msg = create_task()
                    if 'SUCCESS' in msg:
                        tasks = get_tasks()
                        next_run = tasks["\FarFlux_Upload"]["NextRunTime"]
                        result = 4
                        message = f'FarFlux upload task recreated.\nNext run: {next_run}'
                    else:
                        result = 5
                        message = msg
                else:
                    result = 6
                    message = msg
            else:
                result = 9
                message = f'FarFlux upload status: {task_status}'
    return (message, result)

def create_task():
    '''    '''
    check = check_task(take_action=True)
    if check[1] != 0:
        return check[0]
    task_name = 'FarFlux_Upload'
    interval = 15
    task_command = '"C:\\Git\\FarFlux\\.venv\\Scripts\\python.exe C:\\Git\\FarFlux\\upload.py"'
    proc = Popen(f'schtasks /create /sc minute /mo {interval} /tn {task_name} /tr {task_command}',
                 stdout=PIPE)
    output = proc.stdout.read()
    proc.stdout.close()
    msg = output.decode("utf-8")
    if 'SUCCESS' in msg:
        tasks = get_tasks()
        next_run = tasks["\FarFlux_Upload"]["NextRunTime"]
        message = f'FarFlux upload task created.\nNext run: {next_run}'
    return message
