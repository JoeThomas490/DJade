from tkinter import *
from tkinter import ttk, filedialog, messagebox

from pprint import pprint

import eyed3
import os
import shutil
import json

import io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

eyed3.log.setLevel("ERROR")

# def organize(wrkDir, dstDir):
#     workingDirectory = wrkDir
#     print("Current working directory : " + workingDirectory)
#     errorCount = 0
#     successCount = 0

#     destinationDirectory = dstDir

#     for subdir, dirs, files in os.walk(workingDirectory):
#         for file in files:
#             filepath = subdir + os.sep + file
#             if(filepath.endswith(".mp3")):
#                 try:
#                     print("Loading file : " + filepath)
#                     audiofile = eyed3.load(filepath)
#                 except IOError:
#                     print("Cannot find file!")
#                     raise
#                 if audiofile is not None:
#                     if audiofile.tag is not None:
#                         if audiofile.tag.artist is not None and audiofile.tag.title is not None:
#                             artistNameTag = audiofile.tag.artist

#                             artistNameTag = artistNameTag.split("/")
#                             artistName = ""
#                             if(len(artistNameTag) == 2):
#                                 print("Multiple artists found! Pick an option to choose")
#                                 key = input("[A] : {0}  [B] : {1}   [C] : Combine \n Key : ".format(artistNameTag[0], artistNameTag[1]))
#                                 if key == 'A' or key == 'a':
#                                     artistName = artistNameTag[0]
#                                 if key == 'B' or key == 'b':
#                                     artistName = artistNameTag[1]
#                                 if key == 'C' or key == 'c':
#                                     artistName = artistNameTag[0] + ", " + artistNameTag[1]
#                             else:
#                                 artistName = artistNameTag[0]
                            
#                             songName = audiofile.tag.title
#                             print(artistName)

#                             splicedPath = filepath.replace(file, "")
#                             newName = artistName + " - " + songName
#                             for char in '.?!/;:_"':  
#                                 newName = newName.replace(char,'')

#                             newName = newName + ".mp3"  

#                             renamedPath = splicedPath + newName
#                             os.rename(filepath, renamedPath)
#                             print("Renamed file to " + newName)

#                             try:
#                                 os.mkdir(destinationDirectory + "\\" + artistName)
#                                 print("Making directory for " + artistName)
#                             except OSError:
#                                 print("Directory " + artistName + " already exists!")
#                                 if not os.path.isdir(destinationDirectory + "\\" + artistName):
#                                     raise

#                             destinationPath = destinationDirectory + "\\" + artistName + "\\" + newName
#                             print("Moving file to : " + destinationPath)

#                             shutil.move(renamedPath, destinationPath)

#                             successCount = successCount + 1
#                         else:
#                             print("Couldn't find artist or title !")
#                             errorCount = errorCount + 1
#                     else:
#                         print("Song doesn't have tags attached!")
#                         errorCount = errorCount + 1
#                 else:
#                     print("File wasn't loaded properly!")
#                     errorCount = errorCount + 1

#     # try:
#     #     os.rmdir(workingDirectory + "\\" + "downloading")
#     # except OSError:
#     #      print ("'Downloading' folder already deleted!")

#     if errorCount == 0:
#         print("Success!")
#     else:
#         errorMsg = "Error! {0} file(s) couldn't be organized!".format(errorCount)
#         print(errorMsg)
#     treeview.delete(*treeview.get_children())

# def populate():
#     treeview.delete(*treeview.get_children())
#     fileList = []
#     audioFileList = []
#     counter = 0
#     for subdir, dirs, files in os.walk(workingDirectory_entry.get()):
#         for file in files:
#             filepath = subdir + os.sep + file
#             if(filepath.endswith(".mp3")):
#                 fileList.append(filepath)
#                 try:
#                     print("Loading file : " + filepath)
#                     audiofile = eyed3.load(filepath)
#                     audioFileList.append(audiofile)
#                 except IOError:
#                     print("Cannot find file!")
#                     raise

#                 artistName = ""
#                 songName = ""

#                 if audiofile is not None:
#                     if audiofile.tag is not None:
#                         artistName = audiofile.tag.artist
#                         songName = audiofile.tag.title

#                 treeview.insert('', counter , text=filepath, values=(os.path.basename(filepath), artistName, songName))


# def OnDoubleClick(event):
#     item = treeview.focus()
#     print(treeview.item(item))

# treeview = ttk.Treeview(mainframe, selectmode='browse')
# treeview.bind("<Double-1>", OnDoubleClick)

# vsb = ttk.Scrollbar(mainframe, orient="vertical", command=treeview.yview)
# vsb.grid(column = 2, row=2, sticky=(N,S))

# treeview.configure(yscrollcommand=vsb.set)

# treeview['columns'] = ('name', 'artist', 'title')
# treeview.heading("#0", text="Sources", anchor='w')
# treeview.column("#0", anchor='w')
# treeview.heading('name', text='File Name')
# treeview.column('name', anchor ='center', width= 100)
# treeview.heading('artist', text='Artist Tag')
# treeview.column('artist', anchor ='center', width= 100)
# treeview.heading('title', text='Title Tag')
# treeview.column('title', anchor ='center', width= 100)
# treeview.grid(stick = (N,S,W,E), column = 0, row = 2, columnspan=2)
# treeview.columnconfigure(0, weight=1)
# treeview.rowconfigure(0, weight=1)

# populate_btn = ttk.Button(mainframe, text="Populate table", command = lambda:populate())
# organize_btn = ttk.Button(mainframe, text="Organize music!", command = lambda:organize(workingDirectory_entry.get(), destinationDirectory_entry.get()))

# data = loadData()

class Application:
    def __init__(self,master):
        self.master = master
        master.title("Music Organizer")
        master.geometry("1000x500")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.directoryView = DirectoryView(self)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

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
                pprint(data)

                if data["workingDirectory"] is not "":
                    workingDirectory_entry.insert(0, data["workingDirectory"])
                if data["destinationDirectory"] is not "":
                    destinationDirectory_entry.insert(0, data["destinationDirectory"])

            except IOError:
                print("Data file empty!")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # directories = {"workingDirectory" : workingDirectory_entry.get(), "destinationDirectory" : destinationDirectory_entry.get()}
            # print(directories)
            # saveData(directories)
            self.master.destroy()



class DirectoryView:
    def __init__(self,master):
        self.master = master

        self.workingDirectory = StringVar()
        self.destinationDirectory = StringVar()

        self.workingDirectory_entry = ttk.Entry(self.master.mainframe, width = 120, textvariable = self.workingDirectory)
        self.workingDirectory_entry.grid(column=0, row=0, sticky=(N,S, W, E))
        self.workingDirectory_entry.columnconfigure(0, weight=1)
        self.workingDirectory_entry.rowconfigure(0, weight=1)

        self.chooseWorkingDirectory_btn = ttk.Button(self.master.mainframe, text="Choose working directory", command = lambda:self.chooseWorkingDir())
        self.chooseWorkingDirectory_btn.grid(column=1, row=0, sticky=(N,E))

        self.destinationDirectory_entry = ttk.Entry(self.master.mainframe, width = 120, textvariable = self.destinationDirectory)
        self.destinationDirectory_entry.grid(column=0, row=1, sticky=(N,S,W,E))

        self.destinationDirectory_btn = ttk.Button(self.master.mainframe, text="Choose destination", command = lambda:self.chooseDestinationDir())
        self.destinationDirectory_btn.grid(column=1, row=1, sticky=(N,S,W,E))

    def chooseWorkingDir(self):
        self.workingDirectory = filedialog.askdirectory()
        self.workingDirectory_entry.delete(0, END)
        self.workingDirectory_entry.insert(0, self.workingDirectory)
        # saveData({"workingDirectory" : workingDirectory_entry.get(), "destinationDirectory" : destinationDirectory_entry.get()})
        print ("Changed working directory to : " + self.workingDirectory)

    def chooseDestinationDir(self):
        self.destinationDirectory = filedialog.askdirectory()
        self.destinationDirectory_entry.delete(0,END)
        self.destinationDirectory_entry.insert(0, self.destinationDirectory)
        # saveData({"workingDirectory" : workingDirectory_entry.get(), "destinationDirectory" : destinationDirectory_entry.get()})
        print("Changed destination directory to : " + self.destinationDirectory)


root = Tk()

app = Application(root)

root.mainloop()