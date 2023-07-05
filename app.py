from __future__ import print_function
import zipfile
import os.path
import os
import io
from tqdm import tqdm
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload , MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main(folder_id,zip_name):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)
        os.makedirs("temp")
        download_files_from_folder(folder_id,"temp",service)
        zip_folder("temp",zip_name)
        gd_upload(zip_name,folder_id,service)
        delete_folder("temp",zip_name)
        os.rmdir("temp")
    except HttpError as error:
        print(f'An error occurred: {error}')

def download_files_from_folder(folder_id, destination_path,drive_service):
    # Retrieve the files in the specified folder
    files = drive_service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                       fields="files(id, name)", includeItemsFromAllDrives=True,
    supportsAllDrives=True,).execute().get('files', [])
    print(drive_service.files().list())
    if not files:
        print('No files found in the specified folder.')
        return

    # Download each file
    for file in files:
        file_id = file['id']
        file_name = file['name']
        file_path = os.path.join(destination_path, file_name)

        # Download the file
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print(f'Downloading file: {file_name}')
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Downloaded {int(status.progress() * 100)}%')

        # Save the file to the specified destination
        with open(file_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())

        print(f'File downloaded to: {file_path}')

def zip_folder(folder_path, zip_path):
    print("\n\n Making Zip \n\n")
    total_files = 0
    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        progress = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
                progress += 1
                percentage = (progress / total_files) * 100
                print(f'Progress: {progress}/{total_files} ({percentage:.2f}%)')

def gd_upload(file_path,folder,drive_service):
    print("\n\n Uploading Zip to Drive\n\n")
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder],
        'mimeType': '*/*'
    }
    media = MediaFileUpload(file_path,
                            mimetype='*/*',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, supportsAllDrives=True, fields='id').execute()
    print ('File ID: ' + file.get('id'))

def delete_folder(folder_path , zip_file):
    # Get the list of files in the folder
    file_list = os.listdir(folder_path)
    os.remove(zip_file)
    # Iterate over the files and delete each one
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

if __name__ == '__main__':
    while True :
        f = input("Enter Gdrive Folder ID : ")
        z = input("Enter Zip File Name : ")
        main(f,z)
        x = input("Press Any Key To Zip More or 0 (Zero) to Close : ")
        if x == "0":
            break