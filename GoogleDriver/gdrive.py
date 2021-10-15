from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import magic
from PIL import Image

class GoogleDriver():
    def __init__(self, base = None):
        '''will signup us'''
        self.baseId = base
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile("credentials.json")

        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
            self.gauth.SaveCredentialsFile("credentials.json")
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()


    def CheckIfCorrupted(self, loc):
        '''will check if any file is corrupted or not'''
        try:
            im = Image.open(loc)
            im.verify()
            im.close()
            return False
        except (IOError, OSError, Image.DecompressionBombError):
            return True

    def __downloadFolder__(self, folderName, folderId, drive):
        '''will download a folder completely'''
        print("entered folder   ------------------- {}".format(folderName))
        
        if os.path.isdir(folderName) == False:
            os.mkdir(folderName)

        file_list = drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(folderId)}).GetList()
        
        allFilesAndFolder = os.listdir(folderName)

        for file in file_list:
            name = file["title"]
            mimetype = file["mimeType"]
            _id = file["id"]

            if "folder" in mimetype:
                self.__downloadFolder__(folderName+"/"+name, _id, drive)
            else:
                loc = folderName+"/"+name
                if (name in allFilesAndFolder) and self.CheckIfCorrupted(loc) == False:
                    continue
                print("downloading file ------------------- {}".format(loc))
                mem = magic.from_buffer(name, mime=True)
                file.GetContentFile(loc, mimetype=mem)

    def downloadFolder(self, folderName, folderId):
        '''this function will download all the files and folder inside a given folder with given name and file id'''
        drive = GoogleDrive(self.gauth)
        print("------------------- started downloading ---------------------")
        self.__downloadFolder__(folderName, folderId, drive)
        print("------------------------- completed -------------------------")

    def downloadFiles(self, parentId, fileName):
        '''will download all the files with given parentId and fileName'''
        drive = GoogleDrive(self.gauth)
        files = drive.ListFile({'q': "'{}' in parents and title = '{}' and trashed=false".format(parentId, fileName)}).GetList()

        for index, file in enumerate(files):
            mem = magic.from_buffer(fileName, mime=True)
            file.GetContentFile("{}_{}".format(index+1,fileName), mimetype=mem)
    
    def readFile(self, parentId, fileName):
        '''will read the content of all the files with given parentId and fileName'''
        drive = GoogleDrive(self.gauth)
        return drive.ListFile({'q': "'{}' in parents and title = '{}' and trashed=false".format(parentId, fileName)}).GetList()[0].GetContentString()

    def uploadFile(self, parentId, fileLoc):
        '''upload a file from a given location'''
        drive = GoogleDrive(self.gauth)
        fileName = os.path.basename(fileLoc)
        file = drive.CreateFile({'title': fileName, 'parents': [{'id': parentId}]})
        file.SetContentFile(fileLoc)
        file.Upload()
        return file["id"]

    def uploadData(self, parentId, fileName, data):
        '''upload a file with given name and data'''
        drive = GoogleDrive(self.gauth)
        file = drive.CreateFile({'title': fileName, 'parents': [{'id': parentId}]})
        file.SetContentString(data)
        file.Upload()
        return file["id"]

    def __uploadFolder__(self, remoteFolderId, localFolderLoc, drive):
        print("entered folder ------------------- {}".format(localFolderLoc))
        
        allFilesAndFolder = drive.ListFile(
            {'q': "'{}' in parents and trashed=false".format(remoteFolderId)}).GetList()
        
        for file in os.listdir(localFolderLoc):
            if file in allFilesAndFolder:
                continue

            loc = localFolderLoc+"/"+file

            if(os.path.isdir(loc)):
                folder = drive.CreateFile({'title' : file, 'mimeType' : 'application/vnd.google-apps.folder', 'parents': [{'id': remoteFolderId}]})
                folder.Upload()
                self.__uploadFolder__(folder["id"], loc, drive)
            else:
                print("uploading file ------------------- {}".format(loc))
                file = drive.CreateFile({'title': file, 'parents': [{'id': remoteFolderId}]})
                file.SetContentFile(loc)
                file.Upload()


    def uploadFolder(self, remoteFolderId, folderLoc):
        '''this will upload a folder completely to a given folder'''
        drive = GoogleDrive(self.gauth)
        folder = drive.CreateFile({'title' : os.path.basename(folderLoc), 'mimeType' : 'application/vnd.google-apps.folder', 'parents': [{'id': remoteFolderId}]})
        folder.Upload()
        print("------------------- started uploading ---------------------")
        self.__uploadFolder__(folder["id"], folderLoc, drive)
        print("----------------------- completed -------------------------")
        return folder["id"]

    def getAllFiles(self, remoteFolderId=None):
        '''give us dictionary having filename and id pair'''
        if not remoteFolderId:
            remoteFolderId = self.baseId

        drive = GoogleDrive(self.gauth)
        data = {}
        allFilesAndFolder = drive.ListFile(
                {'q': "'{}' in parents and trashed=false".format(remoteFolderId)}).GetList()
            
        for file in allFilesAndFolder:
            data[file["title"]] = file["id"]
        
        return data

    def editFile(self, parentId, fileName, data):
        """this will upload a file to drive with file_name as title and content as data and return the file_name"""
        drive = GoogleDrive(self.gauth)
        file = drive.ListFile({'q': "'{}' in parents and title contains '{}' and trashed=false".format(parentId, fileName)}).GetList()[0]
        
        file.SetContentString(data)
        file.Upload()
        

    def deleteFile(self, parentId, fileName):
        '''will help to delete from a given folder'''
        drive = GoogleDrive(self.gauth)
        file = drive.ListFile({'q': "'{}' in parents and title contains '{}' and trashed=false".format(parentId, fileName)}).GetList()[0]    
        file.Delete()
    
        
if __name__ == "__main__":
    gdrive = GoogleDriver()
    print("------------------------- Thanks For Using -------------------------")
    