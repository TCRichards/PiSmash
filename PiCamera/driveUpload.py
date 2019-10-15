from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


curDir = os.path.dirname(__file__)
credentialsPath = os.path.join(curDir, 'driveCredentials.json')
secretsPath = os.path.join(curDir, 'client_secrets.json')
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = secretsPath


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


def ListSubfolders(parent):
    folders = []
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent['id']}).GetList()
    for f in file_list:
        if f['mimeType'] == 'application/vnd.google-apps.folder':   # if folder
            folders.append({"id": f['id'], "title": f['title']})
    return folders


# Lists out the unique id of each folder
def getTrainingFolder(drive):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for file1 in file_list:
        print('{}: {}'.format(file1['title'], file1['id']))
        if 'PiSmash' in file1['title']:
            subFiles = ListSubfolders(file1)
            for f in subFiles:
                print(f['title'])
                if 'Raw Training Data' in f['title']:
                    return f['id']
    return None


drive = loadCreds()
trainingDirID = getTrainingFolder(drive)


def upload(path):
    file_drive = drive.CreateFile({'title': os.path.basename(path),
                                   "parents": [{"kind": "drive#fileLink", "id": trainingDirID}]
                                   })
    file_drive.SetContentFile(path)
    file_drive.Upload()


if __name__ == '__main__':
    upload(os.path.join(curDir, 'screenShots/shot_5.png'))
