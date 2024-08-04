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

    def retrieve_google_drive_files_for_folder(self, folder_ids):
        files = []
        page_token = None
        query = " or ".join([f"'{folder_id}' in parents" for folder_id in folder_ids])

        while True:
            response = (
                self.service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        
        return files

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


