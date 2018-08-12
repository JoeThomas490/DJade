
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


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("DJade")
        self.master.geometry("1000x500")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.bind("<Escape>", (lambda event: self.on_closing()))

        self.workingDirectory = StringVar()
        self.destinationDirectory = StringVar()

        self.audioFileList = {}

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.treeView = TreeView.TreeView(self)
        self.directoryView = DirectoryView.DirectoryView(self)

        self.saveManager = SaveManager.SaveManager(self)

        loadedData = self.saveManager.loadData()

        self.workingDirectory = loadedData["workingDirectory"]
        self.destinationDirectory = loadedData["destinationDirectory"]

        if self.workingDirectory is not "":
            self.directoryView.workingDirectory_entry.insert(
                0, self.workingDirectory)
        if self.destinationDirectory is not "":
            self.directoryView.destinationDirectory_entry.insert(
                0, self.destinationDirectory)

        self.populateBtn = ttk.Button(
            self.mainframe, text="Populate Table", command=lambda: self.treeView.Populate())
        self.organizeBtn = ttk.Button(
            self.mainframe, text="Organize Music", command=lambda: self.Organize())

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            directories = {"workingDirectory": self.directoryView.workingDirectory_entry.get(
            ), "destinationDirectory": self.directoryView.destinationDirectory_entry.get()}
            self.saveManager.saveData(directories)
            self.master.destroy()

    def Organize(self):

        workingDirectory = self.workingDirectory
        print("Current working directory : " + workingDirectory)
        errorCount = 0
        successCount = 0

        destinationDirectory = self.destinationDirectory

        for subdir, dirs, files in os.walk(workingDirectory):
            for file in files:
                filePath = subdir + os.sep + file
                if(filePath.endswith(".mp3")):
                    try:
                        print("Loading file : " + filePath)
                        audioFile = ID3(filePath)
                    except IOError:
                        print("Cannot find file!")
                        raise
                    if audioFile is not None:
                        if "TIT2" in audioFile and "TPE1" in audioFile:

                            artistNameTag = str(audioFile["TPE1"])
                            artistNameTag = artistNameTag.split("/")
                            artistName = ""
                            artistName = artistNameTag[0]

                            songName = str(audioFile["TIT2"])

                            splicedPath = filePath.replace(file, "")
                            newName = artistName + " - " + songName
                            for char in '.?!/;:_"':
                                newName = newName.replace(char, '')

                            newName = newName + ".mp3"

                            renamedPath = splicedPath + newName
                            os.rename(filePath, renamedPath)
                            print("Renamed file to " + newName)

                            try:
                                os.mkdir(destinationDirectory +
                                         "\\" + artistName)
                                print("Making directory for " + artistName)
                            except OSError:
                                print("Directory " + artistName +
                                      " already exists!")
                                if not os.path.isdir(destinationDirectory + "\\" + artistName):
                                    raise

                            destinationPath = destinationDirectory + "\\" + artistName + "\\" + newName
                            print("Moving file to : " + destinationPath)

                            shutil.move(renamedPath, destinationPath)
                    else:
                        print("File wasn't loaded properly!")
                        errorCount = errorCount + 1


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
