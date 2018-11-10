from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.messagebox import showinfo

import tkinter as tk


class DirectoryView:
    def __init__(self, master):
        self.master = master

        self.workingDirectory_entry = ttk.Entry(
            self.master.mainframe, width=120, textvariable=self.master.workingDirectory)
        self.workingDirectory_entry.grid(column=0, row=1, sticky=(N, S, W, E))
        self.workingDirectory_entry.columnconfigure(0, weight=1)
        self.workingDirectory_entry.rowconfigure(0, weight=1)

        self.chooseWorkingDirectory_btn = ttk.Button(
            self.master.mainframe, text="Choose working directory", command=lambda: self.chooseWorkingDir())
        self.chooseWorkingDirectory_btn.grid(column=1, row=1, sticky=(N, E))

        self.destinationDirectory_entry = ttk.Entry(
            self.master.mainframe, width=120, textvariable=self.master.destinationDirectory)
        self.destinationDirectory_entry.grid(
            column=0, row=2, sticky=(N, S, W, E))

        self.destinationDirectory_btn = ttk.Button(
            self.master.mainframe, text="Choose destination", command=lambda: self.chooseDestinationDir())
        self.destinationDirectory_btn.grid(
            column=1, row=2, sticky=(N, S, W, E))

    def chooseWorkingDir(self):
        newWorkingDir = filedialog.askdirectory()

        if newWorkingDir is "":
            return

        self.master.workingDirectory = newWorkingDir
        self.workingDirectory_entry.delete(0, END)
        self.workingDirectory_entry.insert(0, self.master.workingDirectory)
        print("Changed working directory to : " + self.master.workingDirectory)

    def chooseDestinationDir(self):
        newDestinationDir = filedialog.askdirectory()

        if newDestinationDir is "":
            return

        self.master.destinationDirectory = newDestinationDir
        self.destinationDirectory_entry.delete(0, END)
        self.destinationDirectory_entry.insert(
            0, self.master.destinationDirectory)
        print("Changed destination directory to : " +
              self.master.destinationDirectory)
