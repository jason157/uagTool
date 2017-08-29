# coding=utf-8
from BaseUagLog import *
import tkinter as tk

class HighlightLinesInTextDemo(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.text = tk.Text(self)
		self.text.pack(side="top", fill="both", expand=True)
		self.text.tag_configure("current_line", background="gray")
		self.text.bind("<Motion>", self._highlightline)

	def _highlightline(self, event=None):
		self.text.tag_remove("current_line", 1.0, "end")
		self.text.tag_add("current_line", "current linestart", "current lineend+1c")


app = HighlightLinesInTextDemo()
app.mainloop()