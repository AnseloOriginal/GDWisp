import customtkinter as CTk
import tkinter as Tk



class WeightedSpacing(Tk.Frame):
	def __init__(self,parent,**kwargs):
		super().__init__(parent,**kwargs)
		self.frame_spacing = Tk.Frame()
		self.frame_spacing.grid(row=0,column=1,sticky="ew")

	def apply_spacing(
		self,
		widget: Tk.Widget,
		weight: tuple[int,int] = (3,1),
		space_first = False
	):
		widget_column = 1 if space_first else 0
		space_column = 0 if space_first else 1
		widget.grid(row=0,column=widget_column,sticky="ew")
		self.frame_spacing.grid(column=space_column)
		self.columnconfigure(0,weight=weight[0],uniform="ac")
		self.columnconfigure(1,weight=weight[1],uniform="ac")

