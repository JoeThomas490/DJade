from tkinter import *


class MenuView:
    def __init__(self, master, root):
        self.menuBar = Menu(root)

        # Create a pull down menu
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(
            label="Open directory", command=lambda: self.chooseDirectory())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit", command=lambda: self.quit())

        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        root.config(menu=self.menuBar)

    def hello(self):
        print("Menu test")

    def chooseDirectory(self):
        print("Choose directory")

    def quit(self):
        print("Quit!")
