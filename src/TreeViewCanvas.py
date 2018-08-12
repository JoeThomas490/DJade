import tkinter as tk
import tkinter.font as tkFont


class TreeViewCanvas:
    def __init__(self, master):
        self.master = master
        self.fgCol = '#ecffc4'
        self.bgCol = '#05640e'

        self.InitSelectCanvas(self.fgCol, self.bgCol)

        self.master.bind('<Double-1>', self.SelectItem)

    def InitSelectCanvas(self, fgCol, bgCol):
        self._font = tkFont.Font()

        self._canvas = tk.Canvas(
            self.master, background=bgCol, borderwidth=0)

        self._canvas.text = self._canvas.create_text(
            0, 0, fill=fgCol, anchor='w')

    def SelectItem(self, event):

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

        cellVal = itemValues[int(column[1])-1]

        self.ShowSelectionCanvas(widget, bbox, column, cellVal)

    def ShowSelectionCanvas(self, parent, bbox, column, cellVal):
        x, y, width, height = bbox

        self._canvas.configure(width=width, height=height)

        # Position canvas-textbox in Canvas
        self._canvas.coords(self._canvas.text,
                            15,
                            height*0.5)

        # Update value of canvas-textbox with the value of the selected cell.
        self._canvas.itemconfigure(self._canvas.text, text=cellVal)

        # Overlay Canvas over Treeview cell
        self._canvas.place(in_=parent, x=x, y=y-2)
