from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.messagebox import showinfo
import tkinter.font as tkFont

import tkinter as tk

import os

import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TCON

from src import AudioItem
from pprint import pprint


class TreeView:
    def __init__(self, master):
        self.master = master

        self.treeviewPopup = None

        self.treeview = ttk.Treeview(
            self.master.mainframe, selectmode='extended')

        # self.treeview.bind("<Double-1>", self.OnDoubleClick)
        self.treeview.bind("<Double-1>", self.SelectItem)

        self.vsb = ttk.Scrollbar(
            self.master.mainframe, orient="vertical", command=self.treeview.yview)
        self.vsb.grid(column=2, row=0, sticky=(N, S))

        self.treeview.configure(yscrollcommand=self.vsb.set)

        self.treeview['columns'] = ('name', 'artist', 'title', 'genre')
        self.treeview.heading("#0", text="Sources", anchor='w')
        self.treeview.column("#0", anchor='w', minwidth=0, width=1)
        self.treeview.heading('name', text='File Name')
        self.treeview.column('name', anchor='center', width=200)
        self.treeview.heading('artist', text='Artist Tag')
        self.treeview.column('artist', anchor='center', width=75)
        self.treeview.heading('title', text='Title Tag')
        self.treeview.column('title', anchor='center', width=75)
        self.treeview.heading('genre', text="Genre")
        self.treeview.column('genre', anchor='center', width=100)

        self.treeview.grid(stick=(N, S, W, E), column=0, row=0, columnspan=4)
        self.treeview.columnconfigure(0, weight=1)
        self.treeview.rowconfigure(0, weight=1)

        fgCol = '#ecffc4'
        bgCol = '#05640e'
        self.InitSelectCanvas(fgCol, bgCol)

    def InitSelectCanvas(self, fgCol, bgCol):
        self._font = tkFont.Font()
        self._canvas = tk.Canvas(
            self.treeview, background=bgCol, borderwidth=0)
        self._canvas.text = self._canvas.create_text(
            0, 0, fill=fgCol, anchor='w')

        # self._canvas.bind("<Double-1>", self.OnDoubleClick)

    def SelectItem(self, event):
        self.OnDoubleClick(event)

        # Remove canvas from GUI
        self._canvas.place_forget()

        x, y, widget = event.x, event.y, event.widget

        item = widget.item(widget.focus())
        itemText = item['text']
        itemValues = item['values']
        iid = widget.identify_row(y)
        column = widget.identify_column(x)

        # If selection is not on valid treeview item
        if not iid or not column:
            return

        # If selected item doesn't have any values
        if not len(itemValues):
            return

        if column == '#0' or column == '#1':
            return

        bbox = widget.bbox(iid, column)
        print(bbox)

        cellVal = itemValues[int(column[1])-1]

        self.ShowSelectionCanvas(widget, bbox, column, cellVal)

    def ShowSelectionCanvas(self, parent, bbox, column, cellVal):
        x, y, width, height = bbox

        textw = self._font.measure(cellVal)

        self._canvas.configure(width=width, height=height)

        # Position canvas-textbox in Canvas
        self._canvas.coords(self._canvas.text,
                            15,
                            height*0.5)

        # Update value of canvas-textbox with the value of the selected cell.
        self._canvas.itemconfigure(self._canvas.text, text=cellVal)

        # Overlay Canvas over Treeview cell
        self._canvas.place(in_=parent, x=x, y=y-2)

    def OnDoubleClick(self, event):

        item = self.treeview.item(self.treeview.focus())
        if item["values"] is "":
            return

        columnNum = self.treeview.identify_column(event.x)[1]
        columnNum = int(columnNum)

        if columnNum is not 2 and columnNum is not 3 and columnNum is not 4:
            return

        selectedItem = item["values"][int(columnNum)-1]

        if self.treeviewPopup is None:
            self.treeviewPopup = TreeViewPopup(
                self, item["values"][0], selectedItem, columnNum)

    def DeletePopup(self):
        self.treeviewPopup.window.destroy()
        self.treeviewPopup = None

        self._canvas.place_forget()

    def ConfirmPopupEntry(self, fileName, columnNum, entry):

        audioItem = self.master.audioFileList[fileName]
        audioFile = audioItem.audioFile

        title = audioItem.titleTag
        artist = audioItem.artistTag
        genre = audioItem.genreTag

        # Change ARTIST tag
        if columnNum is 2:
            audioFile["TPE1"] = TPE1(encoding=3, text=entry)

            self.treeview.item(fileName, values=(
                fileName, entry, title, genre))

            audioItem.artist = entry

        # Change TITLE tag
        if columnNum is 3:
            audioFile["TIT2"] = TIT2(encoding=3, text=entry)

            self.treeview.item(fileName, values=(
                fileName, artist, entry, genre))

            audioItem.title = entry

        # Change GENRE tag
        if columnNum is 4:
            audioFile["TCON"] = TCON(encoding=3, text=entry)

            self.treeview.item(fileName, values=(
                fileName, artist, title, entry))

            audioItem.genre = entry

        self.DeletePopup()

        audioFile.save()

    def ClearTreeView(self):
        self.treeview.delete(*self.treeview.get_children())
        self.master.audioFileList.clear()

    def Populate(self):

        self.ClearTreeView()

        for subdir, dirs, files in os.walk(self.master.workingDirectory):
            for file in files:

                filePath = subdir + os.sep + file

                if(filePath.endswith(".mp3")):
                    fileName = os.path.basename(filePath).split(".mp3")[0]
                    try:
                        print("Loading file : " + filePath)
                        audioFile = ID3(filePath)

                    except IOError:
                        print("Cannot find file!")
                        raise

                    artistName = StringVar()
                    songName = StringVar()
                    genreName = StringVar()

                    if audioFile is not None:
                        if "TPE1" in audioFile:
                            artistName = audioFile["TPE1"]
                        else:
                            artistName = "None"

                        if "TIT2" in audioFile:
                            songName = audioFile["TIT2"]
                        else:
                            songName = "None"

                        if "TCON" in audioFile:
                            genreName = audioFile["TCON"]
                        else:
                            genreName = "None"

                    audioItem = AudioItem.AudioItem(
                        self, filePath, fileName, audioFile, artistName, songName, genreName)

                    self.master.audioFileList[fileName] = audioItem

                    self.treeview.insert('', 'end', fileName, text=filePath, values=(
                        fileName, artistName, songName, genreName))


class TreeViewPopup:
    def __init__(self, master, fileName, selectedItem, columnNum):

        self.master = master

        self.window = tk.Toplevel()
        self.window.wm_title("Edit Tag")
        self.window.wm_attributes("-topmost", 1)

        self.window.protocol("WM_DELETE_WINDOW", self.master.DeletePopup)

        self.window.geometry("%dx%d%+d%+d" % (300, 100, 150, 250))

        self.tagLbl = tk.Label(self.window, text="Tag")
        self.tagLbl.grid(row=0, column=0)

        self.tagEntry = tk.Entry(self.window)
        self.tagEntry.grid(row=0, column=1, sticky=(N, E))
        self.tagEntry.delete(0, END)
        self.tagEntry.insert(0, selectedItem)
        self.tagEntry.focus_set()

        # Dropdown menu test

        # self.optionMenuVar = StringVar()
        # self.optionMenu = ttk.OptionMenu(
        #     self.window, self.optionMenuVar, 'one', 'two', 'three')
        # self.optionMenu.grid(row=0, column=2)

        self.confirmBtn = ttk.Button(self.window, text="Confirm", command=lambda: self.master.ConfirmPopupEntry(
            fileName, columnNum, self.tagEntry.get()))
        self.confirmBtn.grid(row=1, column=0, sticky=(S, W))

        self.cancelBtn = ttk.Button(
            self.window, text="Cancel", command=lambda: self.master.DeletePopup())
        self.cancelBtn.grid(row=1, column=1, sticky=(S, E))

        for child in self.window.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.window.bind("<Return>", (lambda event: self.master.ConfirmPopupEntry(
            fileName, columnNum, self.tagEntry.get())))
