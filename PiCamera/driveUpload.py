from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from pathlib import Path

curDir = os.path.dirname(__file__)
projectDir = Path(curDir).parent
credentialsPath = os.path.join(curDir, 'driveCredentials.json')


def loadCreds():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(credentialsPath)
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(credentialsPath)

    drive = GoogleDrive(gauth)
    return drive


# Lists out the unique id of each folder
def getTrainingFolder(drive):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if 'Training' in file1['title']:
            return file1['id']
    return None


drive = loadCreds()
trainingDirID = getTrainingFolder(drive)


def upload(path, name):
    # Make sure the destination name has the proper file extension
    if '.png' not in name:
        name += '.png'
    file_drive = drive.CreateFile({'title': name,
                                   "parents": [{"kind": "drive#fileLink", "id": trainingDirID}]
                                   })
    file_drive.SetContentFile(path)
    file_drive.Upload()


if __name__ == '__main__':
    upload(os.path.join(curDir, 'screenShots/shot_5.png'), 'UploadTest.png')