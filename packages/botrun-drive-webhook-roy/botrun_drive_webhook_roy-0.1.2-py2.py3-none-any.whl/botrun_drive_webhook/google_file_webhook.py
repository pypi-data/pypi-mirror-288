from google.oauth2 import service_account
from googleapiclient.discovery import build
import time
import requests
import urllib.parse
import hashlib

def google_file_webhook(
    service_account_file,
    file_id,
    webhook_url_format,
    scopes=['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/documents.readonly'],
    check_interval=5
):  
    def get_file_info(drive_service, docs_service, file_id):
        file_info = drive_service.files().get(fileId=file_id, fields="id, name, modifiedTime").execute()
        
        # 獲取文檔內容的前100個字符
        doc_content = docs_service.documents().get(documentId=file_id).execute()
        content_sample = doc_content.get('body', {}).get('content', [])
        #因為要監控內容是否有改變，所以這裡使用hash，如果內容有改變，hash值也會改變
        content_text=hashlib.sha256(f"{content_sample}".encode('utf-8')).hexdigest()
        #print(f"[content_sample]=\n{content_text}")

        file_info['content_sample'] = content_text
        return file_info

    def notify_webhook(file_id, file_name, updated_time):
        full_url = webhook_url_format.format(
            file_id=urllib.parse.quote(file_id),
            file_name=urllib.parse.quote(file_name),
            updated_time=urllib.parse.quote(updated_time)
        )
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                print(f"Webhook notified successfully for file {file_name}")
            else:
                print(f"Failed to notify webhook for file {file_name}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error notifying webhook: {str(e)}")

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes)

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    old_state = get_file_info(drive_service, docs_service, file_id)
    new_state=old_state
    
    print(f"Monitoring the change of file={old_state['name']}, [content_sample]={old_state['content_sample']}")
    
    error_count=0
    while True:
        try:
            print(f"""Checking for updates...{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}""")
            new_state = get_file_info(drive_service, docs_service, file_id)
            #print(new_state)
            if (new_state['modifiedTime'] != old_state['modifiedTime'] or
                new_state['content_sample'] != old_state['content_sample']):
                print(f"Content changed! file={new_state['name']}, time={new_state['modifiedTime']}, fileid={new_state['id']} ,[content_sample]={new_state['content_sample']}")
                notify_webhook(new_state['id'], new_state['name'], new_state['modifiedTime'])
                print("webhook done.")
            else:
                print("no change")

            old_state = new_state
            error_count=0
            time.sleep(check_interval)
        except Exception as e:
            error_count+=1
            print(f"[google_file_webhook] An error occurred ({error_count}) : {e}")
            if error_count>2:
                print(f"[google_file_webhook] Error count>3, skip file={new_state['name']}")
                old_state = new_state
            time.sleep(check_interval)
            if error_count>100:
                print(f"[google_file_webhook] Error count>100, stop monitoring.")
                break

# 使用示例
if __name__ == '__main__':
    google_file_webhook(
        service_account_file='path/to/your/service_account_file.json',
        file_id='your_google_doc_file_id_here',
        webhook_url_format='https://your-webhook-url.com/hook?id={file_id}&name={file_name}&updated={updated_time}'
    )