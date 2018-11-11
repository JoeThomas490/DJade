
'''
Import tkinter stuff
'''
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.messagebox import showinfo

import tkinter as tk


'''
Import src modules
'''
from src import TreeView
from src import SaveManager
from src import DirectoryView
from src import AudioItem

'''
Import system modules
'''
from pprint import pprint

import os
import shutil
import json
import io

'''
Import mutagen library
'''

import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1

'''
END IMPORT
'''


##########################################################
# Main application class. Deals with initialising the canvas view and also
# handling main operations such as organizing/moving files around
##########################################################


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("DJade")
        self.master.geometry("1000x500")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.bind("<Escape>", (lambda event: self.on_closing()))

        # Create working/destination directory vars
        self.workingDirectory = StringVar()
        self.destinationDirectory = StringVar()

        self.audioFileList = {}

        # Create the main frame view
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # Create tree view (shows files)
        self.treeView = TreeView.TreeView(self)

        # Create directory view (to select working/destination dirs)
        self.directoryView = DirectoryView.DirectoryView(self)

        self.saveManager = SaveManager.SaveManager(self)

        self.init_save_data()

        self.populateBtn = ttk.Button(
            self.mainframe, text="Populate Table", command=lambda: self.treeView.Populate())
        self.organizeBtn = ttk.Button(
            self.mainframe, text="Organize Music", command=lambda: self.Organize())

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    ##########################################################
    # Initialises save data (previous working/destination directorys)
    ##########################################################

    def init_save_data(self):

        loadedData = self.saveManager.loadData()
        self.workingDirectory = loadedData["workingDirectory"]
        self.destinationDirectory = loadedData["destinationDirectory"]

        if self.workingDirectory is not "":
            self.directoryView.workingDirectory_entry.insert(
                0, self.workingDirectory)
        if self.destinationDirectory is not "":
            self.directoryView.destinationDirectory_entry.insert(
                0, self.destinationDirectory)

    ##########################################################
    # Function called when the application is closed
    ##########################################################

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            directories = {"workingDirectory": self.directoryView.workingDirectory_entry.get(
            ), "destinationDirectory": self.directoryView.destinationDirectory_entry.get()}
            self.saveManager.saveData(directories)
            self.master.destroy()

    ##########################################################
    # Main organize function. Moves files, and sets meta data.
    # TODO : This needs to be split up into smaller functions
    ##########################################################

    def Organize(self):

        print("Current working directory : " + self.workingDirectory)

        errorCount = 0
        successCount = 0
        totalFiles = 0

        # Walk through the current working directory and get every
        # file
        for subdir, dirs, files in os.walk(self.workingDirectory):
            for file in files:
                # Create the absolute filepath for this file
                filePath = subdir + os.sep + file

                totalFiles = totalFiles + 1

                # If this file ends with .mp3
                # TODO : Make this work with other file types
                if(filePath.endswith(".mp3")):
                    # Try and load the current file
                    try:
                        print("Loading file : " + filePath)
                        audioFile = ID3(filePath)
                    except IOError:
                        print("Cannot find file!")
                        raise

                    # If the file was loaded successfully
                    if audioFile is not None:
                        # And the file has certain tags accessible
                        if "TIT2" in audioFile and "TPE1" in audioFile:

                            # Get the artist tag and get first artist if multiple
                            artistNameTag = str(audioFile["TPE1"])
                            artistNameTag = artistNameTag.split("/")
                            artistName = ""
                            artistName = artistNameTag[0]

                            # Get the song name tag
                            songName = str(audioFile["TIT2"])

                            splicedPath = filePath.replace(file, "")

                            # Create the new name for the file
                            newName = artistName + " - " + songName
                            # Remove any special characters that will conflict with
                            # moving new file
                            for char in '.?!/;:_"':
                                newName = newName.replace(char, '')

                            # Add file ending to new name
                            newName = newName + ".mp3"

                            # Create the new path with the new file name
                            # TODO : Make the new file renaming configurable
                            # i.e artist-song, song, song-artist
                            renamedPath = splicedPath + newName

                            # Rename the file
                            os.rename(filePath, renamedPath)
                            print("Renamed file to " + newName)

                            # Try and make a new directory for the artist
                            try:
                                os.mkdir(self.destinationDirectory +
                                         "\\" + artistName)
                                print("Making directory for " + artistName)
                            # If the directory already exists
                            except OSError:
                                print("Directory " + artistName +
                                      " already exists!")
                                if not os.path.isdir(self.destinationDirectory + "\\" + artistName):
                                    raise

                            # Create the destination path out of the artist name and new name
                            destinationPath = self.destinationDirectory + "\\" + artistName + "\\" + newName
                            print("Moving file to : " + destinationPath)

                            # Move the file
                            shutil.move(renamedPath, destinationPath)

                            successCount = successCount + 1
                        else:
                            print("No tags found on file")
                            errorCount = errorCount + 1
                    else:
                        print("File wasn't loaded properly!")
                        errorCount = errorCount + 1

        print("Files moved : ", successCount)
        print("Errors : ", errorCount)

        self.treeView.Populate()
        # print("Success rate:", totalFiles / successCount)


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
