import time
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import uuid
import re

SCOPES = ['https://www.googleapis.com/auth/drive']

def google_drive_callback(service_account_file, 
                         folder_id, 
                         webhook_url, 
                         force_reset_webhook_channel=False,
                         check_interval=10, 
                         is_get_file_path=False,
                         file_pattern='*', 
                         call_back_function=None, 
                         is_loop_exec=False,
                         notification_info_path="./users/notification_info.json"
                        ):
    try:
        print("==============init_google_drive_webhook=========================================")
        print(f"step 1. init_google_drive_webhook... ")
        init_google_drive_webhook(service_account_file=service_account_file,
                                  folder_id=folder_id,
                                  webhook_url=webhook_url,
                                  force_reset_webhook_channel=force_reset_webhook_channel,
                                  notification_info_path="./users/notification_info.json"
                                  )
        
        print("==============check_folder_notifications=========================================")
        print(f"step 2. Start check_folder_notifications... every {check_interval}sec")
        check_folder_notifications(service_account_file=service_account_file, 
                               folder_id=folder_id, 
                               check_interval=check_interval, 
                               is_get_file_path=is_get_file_path,
                               file_pattern=file_pattern, 
                               call_back_function=call_back_function,
                               is_loop_exec=is_loop_exec,
                               notification_info_path="./users/notification_info.json"
                               )

        return 

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def init_google_drive_webhook(service_account_file, 
                        folder_id, 
                        webhook_url, 
                        force_reset_webhook_channel=False,
                        notification_info_path="./users/notification_info.json"
                         ):
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    try:
        os.makedirs("./users/", exist_ok=True)
        if os.path.exists(notification_info_path):
            with open(notification_info_path, 'r') as f:
                info = json.load(f)
            
            current_time = datetime.datetime.now()
            expiration_time = datetime.datetime.fromtimestamp(int(info['expiration']) / 1000)

            if not force_reset_webhook_channel and current_time < expiration_time:
                print(f"Existing notification is still valid. Using the current one. expiration_time={expiration_time}")
                return info
            else:
                # stop the notification channel for reseting
                try:
                    service.channels().stop(body={
                        'id': info['channelId'],
                        'resourceId': info['resourceId']
                    }).execute()
                    print(f"Stopped expired notification: {info['channelId']}")
                except HttpError as error:
                    print(f"Error stopping expired notification: {error}")
            
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error reading notification_info.json: {e}")
        print("Creating new notification_info.json and establishing new connection.")

    channel = {
        'id': f"google_drive_webhook_{str(uuid.uuid4())}",
        'type': 'web_hook',
        'address': webhook_url,
        'expiration': int((datetime.datetime.now() + datetime.timedelta(days=7)).timestamp() * 1000)
    }

    try:
        response = service.files().watch(
            fileId=folder_id,
            body=channel
        ).execute()

        print(f"New notification channel set up: {json.dumps(response, indent=2)}")
    
        start_page_token = service.changes().getStartPageToken().execute()

        new_info = {
            'channelId': response['id'],
            'resourceId': response['resourceId'],
            'expiration': response['expiration'],
            'startPageToken': start_page_token['startPageToken']
        }

        with open(notification_info_path, 'w') as f:
            json.dump(new_info, f)
        
        print(f"Initial start page token: {start_page_token['startPageToken']}")

        return new_info

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def get_file_path(service, file_id, root_folder_id):
    path = []
    while True:
        file = service.files().get(fileId=file_id, fields='name,parents').execute()
        path.insert(0, file['name'])
        if 'parents' not in file or file['parents'][0] == root_folder_id:
            return '/'.join(path)
        file_id = file['parents'][0]

def check_folder_notifications(service_account_file, 
                               folder_id, 
                               check_interval=10, 
                               is_get_file_path=False,
                               file_pattern='*', 
                               call_back_function=None,
                               is_loop_exec=False,
                               notification_info_path="./users/notification_info.json"
                               ):
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_regex = re.compile(file_pattern.replace('*', '.*'))

    error_count=0
    while True:
        try:
            with open(notification_info_path, 'r') as f:
                info = json.load(f)
            start_page_token = info['startPageToken']

            response = service.changes().list(
                pageToken=start_page_token,
                spaces='drive',
                fields='newStartPageToken, changes(fileId, time, file(name, parents))'
            ).execute()

            if 'newStartPageToken' in response:
                new_start_page_token = response['newStartPageToken']
                info['startPageToken'] = new_start_page_token
                with open(notification_info_path, 'w') as f:
                    json.dump(info, f)
                
                str_change_info = "Change detected!" if start_page_token != new_start_page_token else "No change."
                print(f"[check_folder_notifications] Get new page token: {new_start_page_token}  status={str_change_info}")
                start_page_token = new_start_page_token
            
            
            #print("==============change=====")
            #demo_change = response.get('changes', [])
            #print(demo_change)
            #print("==============change end====")


            for change in response.get('changes', []):
                print(f"Changed file:")
                file_id = change.get('fileId', 'N/A')
                updated_time = change.get('time', 'N/A')
                print(f"File ID: {file_id}")
                print(f"Change Time: {updated_time}")
                
                if 'file' in change:
                    file_info = change['file']
                    file_name = file_info.get('name', 'N/A')
                    parents = file_info.get('parents', 'N/A')
                    print(f"File Name: {file_name}")
                    print(f"Parent Folder IDs: {', '.join(parents)}")

                    if is_get_file_path:
                        if folder_id in parents:
                            file_path = get_file_path(service, file_info['id'], folder_id)
                            print(f"File Path: {file_path}")

                    if call_back_function and file_regex.match(file_name):
                        # Call the callback function
                        call_back_function(file_id, file_name, updated_time, parents, file_path if is_get_file_path else None)
                        print("Callback function executed.")
                else:
                    print("File information not available (possibly deleted)")

                print("---")
            error_count=0
            print(f"""Done. time={time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")

            # 判斷是否要回權重複執行
            if not is_loop_exec: 
                break

            time.sleep(check_interval)

        except Exception as e:
            error_count+=1
            print(f"[check_folder_notifications] An error occurred: {e}")
            # If the error is due to channel expiration, reinitialize the webhook
            if "Channel has expired" in str(e):
                print("Channel has expired. Reinitializing webhook...")
                init_google_drive_webhook(service_account_file, folder_id, info['channelId'], force_reset_webhook_channel=True)
                break # Break the loop to reinitialize the webhook

            print(f"""Exception! time={time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")
            time.sleep(check_interval)
            if error_count>100:
                print(f"[check_folder_notifications] Error count>100, stop monitoring....ERROR!")
                break
    

# Example usage:
# def my_callback(file_id, file_name, updated_time, file_path=None):
#     print(f"File {file_name} (ID: {file_id}) was updated at {updated_time}")
#     if file_path:
#         print(f"File path: {file_path}")

# google_drive_callback(
#     service_account_file='path/to/service_account.json',
#     folder_id='your_folder_id',
#     webhook_url='your_webhook_url',
#     is_get_file_path=True,
#     file_pattern='*.txt',
#     call_back_function=my_callback
# )


# interface for get the update queue
def get_update_queue(time=None):
    json_queue=[
                {
                    "collection_id": "1SKuM-Ld9yu4Om372nZZBdSQ7BBt7g1l1",
                    "file_id": "1VinOeWHfSjyyexqn2coQr6DbuZxslfKgCuqiXcUecOk",
                    "file_name": "testfile",
                    "updated_time": "2024-08-06T01:21:47.363Z"
                }
        ]
    print("[get_update_queue] done")
    return json_queue

def finish_queue_process(collection_id=None, file_id=None, updated_time=None):
    info=f"[finish_queue_process] done"
    print(info)
    return info