from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import httpx

class UserGoogleDrive:
    def __init__(self, user):
        self.user = user
        user_identities = user['identities']
        google_identity = [identity for identity in user_identities if identity['provider'] == 'google-oauth2'][0]
        self.access_token = google_identity['access_token']

        creds = Credentials(token=self.access_token)
        self.service = build('drive', 'v3', credentials=creds)

    def list_files_in_folder(self, folder_id):
        all_files = []
        query = f"'{folder_id}' in parents and trashed = false"
        page_token = None

        while True:
            results = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token
            ).execute()
            items = results.get('files', [])

            for item in items:
                if item['mimeType'] != 'application/vnd.google-apps.folder':
                    all_files.append(item)
                else:
                    all_files.extend(self.list_files_in_folder(item['id']))

            page_token = results.get('nextPageToken')
            if not page_token:
                break

        return all_files

    def retrieve_google_drive_files_for_folder(self, folder_ids):
        all_files = []
        for folder_id in folder_ids:
            all_files.extend(self.list_files_in_folder(folder_id))
        return all_files

    def retrieve_google_drive_files(self, file_ids):
        files = []
        for file_id in file_ids:
            file = self.service.files().get(fileId=file_id).execute()
            files.append(file)

        return files

    def retrieve_folder_id_by_name(self, service, folder_name):
        response = service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        folders = response.get('files', [])
        if not folders:
            raise Exception(f"Folder '{folder_name}' not found.")

        return folders[0]['id']
    
    async def download_file(self, file_id):
        url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        # To-Do needs better error handling
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.content
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
        except Exception as exc:
            print(f"An error occurred: {str(exc)}")

        return None


