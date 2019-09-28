from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
os.environ['TZ'] = 'EST'   # Make sure we're on Eastern time (although if we're doing this abroad that'd be sick)
from inspect import getsourcefile
import sys
import errno
from threading import Thread


current_path = os.path.abspath(getsourcefile(lambda: 0))
curDir = os.path.dirname(current_path)
parent_dir = curDir[:curDir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

from ScreenClassifier import ScreenModel
labels = ScreenModel.screenDict.keys()
from definitions import ROOT_DIR


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
# If getProjectFolder is true, this simply returns the ID for the PiSmash project directory
def getFolderID(drive, dirName, getProjectFolder=False):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()  # Google Drive root directory

    for file1 in file_list:
        if 'PiSmash Training Data' in file1['title']:
            if getProjectFolder:
                return file1['id']

            subFolders = ListSubfolders(file1)
            for f in subFolders:
                print(f['title'])
                if dirName in f['title']:
                    return f['id']  # Returns the ID that drive uses to access it from anywhere
    return None


def listDriveFolder(drive, label):
    rootFileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    for driveObj in rootFileList:
        if 'PiSmash Training Data' in driveObj['title']:
            subFolders = ListSubfolders(driveObj)

            for subFolder in subFolders:    # Look through each folder in the project directory
                if label in subFolder['title']:   # Match our desired directory with the proper one in drive
                    targetDirID = subFolder['id']   # Get the correct directory's ID
                    subFiles = drive.ListFile({'q': "'{}' in parents and trashed=false".format(targetDirID)}).GetList()     # These will be the individual images in our application
                    return subFiles


drive = loadCreds()
PiSmashID = getFolderID(drive, '', getProjectFolder=True)


# Returns the most recent file added to a directory excluding the last file checked
def getMostRecentFile(directory):
    fileNames = os.listdir(directory)
    if not fileNames:
        return None
    # os.path.gentime resets every time a file is examined by the program, so exclude if it's the same
    # or else we never move
    sortedNames = sorted(fileNames, key=lambda x: os.path.getctime(os.path.join(directory, x)))

    # If there are multiple options, the second one is the one we want (first is always a repeat)
    return os.path.join(directory, sortedNames[0])   # If only one option, then take it


# Automatically updates the local project with new training data
# pathList = list of paths from project directory whose names match the locations inside Google Drive/PiSmash Training Data
def updateLocalData(drive, localDir='ScreenClassifier/trainingImages/'):

    def updateCategory(label):
        categoryFolder = os.path.join(localDir, label)  # This is the local folder of images of each classification
        try:
            os.mkdir(categoryFolder)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        currentImages = os.listdir(categoryFolder)

        imageDicts = listDriveFolder(drive, label)  # Each imageDict is dictionary with title, id and other info about the file
        for image in imageDicts:
            if image['title'] not in currentImages:  # If the image was added since our last Update
                image.GetContentFile(os.path.join(categoryFolder, image['title']))
                print('Downloading {} from {}'.format(image['title'], label))

    liveThreads = []
    for label in labels:    # Download from each folder simultaneously using threading
        downloadThread = Thread(target=updateCategory, args=(label, ), daemon=False)    # Daemon=False prevents program from ending
        downloadThread.start()
        liveThreads.append(downloadThread)
    for t in liveThreads:
        t.join()


# Uploads the specified file to drive
def upload(path):
    trainingDirID = getFolderID(drive, 'Raw Training Data')
    file_drive = drive.CreateFile({'title': os.path.basename(path),
                                   "parents": [{"kind": "drive#fileLink", "id": trainingDirID}]
                                   })
    file_drive.SetContentFile(path)
    file_drive.Upload()


if __name__ == '__main__':
    trainingDir = os.path.join(ROOT_DIR, 'ScreenClassifier/trainingImages/')
    drive = loadCreds()
    updateLocalData(drive, localDir=trainingDir)
