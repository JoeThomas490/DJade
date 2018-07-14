from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.messagebox import showinfo

import tkinter as tk


from pprint import pprint

import eyed3
import os
import shutil
import json

import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1

import io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

eyed3.log.setLevel("ERROR")

'''
Class : MusicItem
Info  : Holds data to do with each music file, containing the path, filename and mp3 tags
'''
class MusicItem:
    pass

class Application:
     def __init__(self,master):
        self.master = master
        self.master.title("Music Organizer")
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

        self.treeView = TreeView(self)
        self.directoryView = DirectoryView(self)

        self.saveManager = SaveManager(self)

        loadedData = self.saveManager.loadData()

        self.workingDirectory = loadedData["workingDirectory"]
        self.destinationDirectory = loadedData["destinationDirectory"]

        if self.workingDirectory is not "":
            self.directoryView.workingDirectory_entry.insert(0, self.workingDirectory)
        if self.destinationDirectory is not "":
            self.directoryView.destinationDirectory_entry.insert(0, self.destinationDirectory)

        self.populateBtn = ttk.Button(self.mainframe, text="Populate Table", command = lambda:self.treeView.Populate())
        self.organizeBtn = ttk.Button(self.mainframe, text="Organize Music", command = lambda:self.Organize())


        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            directories = {"workingDirectory" : self.directoryView.workingDirectory_entry.get(), "destinationDirectory" : self.directoryView.destinationDirectory_entry.get()}
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
                                newName = newName.replace(char,'')

                            newName = newName + ".mp3"  

                            renamedPath = splicedPath + newName
                            os.rename(filePath, renamedPath)
                            print("Renamed file to " + newName)

                            try:
                                os.mkdir(destinationDirectory + "\\" + artistName)
                                print("Making directory for " + artistName)
                            except OSError:
                                print("Directory " + artistName + " already exists!")
                                if not os.path.isdir(destinationDirectory + "\\" + artistName):
                                    raise

                            destinationPath = destinationDirectory + "\\" + artistName + "\\" + newName
                            print("Moving file to : " + destinationPath)

                            shutil.move(renamedPath, destinationPath)
                    else:
                        print("File wasn't loaded properly!")
                        errorCount = errorCount + 1


class DirectoryView:
    def __init__(self,master):
        self.master = master

        self.workingDirectory_entry = ttk.Entry(self.master.mainframe, width = 120, textvariable = self.master.workingDirectory)
        self.workingDirectory_entry.grid(column=0, row=1, sticky=(N,S, W, E))
        self.workingDirectory_entry.columnconfigure(0, weight=1)
        self.workingDirectory_entry.rowconfigure(0, weight=1)

        self.chooseWorkingDirectory_btn = ttk.Button(self.master.mainframe, text="Choose working directory", command = lambda:self.chooseWorkingDir())
        self.chooseWorkingDirectory_btn.grid(column=1, row=1, sticky=(N,E))

        self.destinationDirectory_entry = ttk.Entry(self.master.mainframe, width = 120, textvariable = self.master.destinationDirectory)
        self.destinationDirectory_entry.grid(column=0, row=2, sticky=(N,S,W,E))

        self.destinationDirectory_btn = ttk.Button(self.master.mainframe, text="Choose destination", command = lambda:self.chooseDestinationDir())
        self.destinationDirectory_btn.grid(column=1, row=2, sticky=(N,S,W,E))

    def chooseWorkingDir(self):
        newWorkingDir = filedialog.askdirectory()

        if newWorkingDir is "":
            return

        self.master.workingDirectory = newWorkingDir
        self.workingDirectory_entry.delete(0, END)
        self.workingDirectory_entry.insert(0, self.master.workingDirectory)
        print ("Changed working directory to : " + self.master.workingDirectory)

    def chooseDestinationDir(self):
        newDestinationDir = filedialog.askdirectory()

        if newDestinationDir is "":
            return

        self.master.destinationDirectory = newDestinationDir
        self.destinationDirectory_entry.delete(0,END)
        self.destinationDirectory_entry.insert(0, self.master.destinationDirectory)
        print("Changed destination directory to : " + self.master.destinationDirectory)

class TreeView:
    def __init__(self,master):
        self.master = master

        self.treeviewPopup = None

        self.treeview = ttk.Treeview(self.master.mainframe, selectmode='browse')
        self.treeview.bind("<Double-1>", self.OnDoubleClick)

        self.vsb = ttk.Scrollbar(self.master.mainframe, orient="vertical", command=self.treeview.yview)
        self.vsb.grid(column = 2, row=0, sticky=(N,S))

        self.treeview.configure(yscrollcommand=self.vsb.set)

        self.treeview['columns'] = ('name', 'artist', 'title')
        self.treeview.heading("#0", text="Sources", anchor='w')
        self.treeview.column("#0", anchor='w')
        self.treeview.heading('name', text='File Name')
        self.treeview.column('name', anchor ='center', width= 100)
        self.treeview.heading('artist', text='Artist Tag')
        self.treeview.column('artist', anchor ='center', width= 100)
        self.treeview.heading('title', text='Title Tag')
        self.treeview.column('title', anchor ='center', width= 100)
        self.treeview.grid(stick = (N,S,W,E), column = 0, row = 0, columnspan=2)
        self.treeview.columnconfigure(0, weight=1)
        self.treeview.rowconfigure(0, weight=1)

    def OnDoubleClick(self,event):
        item = self.treeview.item(self.treeview.focus())
        if item["values"] is "":
            return

        columnNum = self.treeview.identify_column(event.x)[1]
        columnNum = int(columnNum)

        if columnNum is not 2 and columnNum is not 3:
            return

        selectedItem = item["values"][int(columnNum)-1]

        if self.treeviewPopup is None:
            self.treeviewPopup = TreeViewPopup(self, item["values"][0],selectedItem,columnNum)

    def DeletePopup(self):
        self.treeviewPopup.window.destroy()
        self.treeviewPopup = None

    def ConfirmPopupEntry(self, fileName, columnNum, entry):

        audioFile = self.master.audioFileList[fileName]

        #Change ARTIST tag
        if columnNum is 2:
            audioFile["TPE1"] = TPE1(encoding=3, text=entry)

        #Change TITLE tag
        if columnNum is 3:
            audioFile["TIT2"] = TIT2(encoding=3, text=entry)

        self.DeletePopup()

        audioFile.save()

        # self.treeview.insert('', counter , text=filePath, values=(fileName, artistName, songName))
        self.Populate()
        

    def ClearTreeView(self):
        self.treeview.delete(*self.treeview.get_children())
        self.master.audioFileList.clear()

    def Populate(self):
        
        self.ClearTreeView()
        counter = 0

        for subdir, dirs, files in os.walk(self.master.workingDirectory):
            for file in files:

                filePath = subdir + os.sep + file

                if(filePath.endswith(".mp3")):
                    fileName = os.path.basename(filePath).split(".mp3")[0]
                    try:
                        print("Loading file : " + filePath)
                        audioFile = ID3(filePath)
                        self.master.audioFileList[fileName] = audioFile

                    except IOError:
                        print("Cannot find file!")
                        raise

                    artistName = StringVar()
                    songName = StringVar()

                    if audioFile is not None:
                        if "TPE1" in audioFile:
                            artistName = audioFile["TPE1"]
                        else:
                            artistName = "None"

                        if "TIT2" in audioFile:
                            songName = audioFile["TIT2"]
                        else:
                            songName = "None"

                   

                    self.treeview.insert('', counter , text=filePath, values=(fileName, artistName, songName))

class TreeViewPopup:
    def __init__(self, master, fileName, selectedItem,columnNum):

        self.master = master

        self.window = tk.Toplevel()
        self.window.wm_title("Edit Tag")
        self.window.wm_attributes("-topmost",1)

        self.window.protocol("WM_DELETE_WINDOW", self.master.DeletePopup)

        self.window.geometry("%dx%d%+d%+d" % (300, 100, 150, 250))

        self.tagLbl = tk.Label(self.window, text="Tag")
        self.tagLbl.grid(row=0, column=0)

        self.tagEntry = tk.Entry(self.window)
        self.tagEntry.grid(row=0, column=1, sticky=(N,E))
        self.tagEntry.delete(0,END)
        self.tagEntry.insert(0, selectedItem)
        self.tagEntry.focus_set()

        self.confirmBtn = ttk.Button(self.window, text="Confirm", command=lambda:self.master.ConfirmPopupEntry(fileName, columnNum, self.tagEntry.get()))
        self.confirmBtn.grid(row=1, column=0, sticky=(S,W))

        self.cancelBtn = ttk.Button(self.window, text="Cancel", command=lambda:self.master.DeletePopup())
        self.cancelBtn.grid(row=1, column= 1, sticky=(S,E))        

        for child in self.window.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.window.bind("<Return>", (lambda event:self.master.ConfirmPopupEntry(fileName, columnNum, self.tagEntry.get())))

class SaveManager:
    def __init__(self, master):
        self.master = master

    def saveData(self,data):
        with io.open('data.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))

    def loadData(self):
        with open('data.json', 'r', encoding='utf8') as outfile:
            try:
                data = json.load(outfile)
                return data

            except IOError:
                print("Data file empty!")

root = Tk()
app = Application(root)
root.mainloop()