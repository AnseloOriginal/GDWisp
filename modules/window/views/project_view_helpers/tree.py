from __future__ import annotations
from typing import Literal, Callable
import customtkinter
from modules.media.image import ICON
from modules.config.colors import tree_theme
type TreeStructure = dict[str, TreeStructure | str]

button_open = customtkinter.CTkImage(ICON["expanded"])
button_closed = customtkinter.CTkImage( ICON["contracted"])
def button(
	master: customtkinter.CTkBaseClass, 
	text: str, 
	icon: Literal["open", "expanded", "contracted"] = "open"
):
	image = customtkinter.CTkImage(ICON[icon])
	butn = customtkinter.CTkButton(
		master,
		text=text,
		text_color=tree_theme["text_color"],
		fg_color="transparent",
		hover_color=tree_theme["hover_color"],
		image=image,
		compound="left",
		anchor="w",
    	font=(None,14),

	)
	return butn

class Tree(customtkinter.CTkScrollableFrame):

	def __init__(self, master, tree: TreeStructure, showCount: bool):
		super().__init__(master)
		mainFrame = self.to_branch(tree,self)
		mainFrame.grid(column=0, row=0)
		self.callables: list[Callable[[str]]] = []

	def to_branch(self,tree: TreeStructure,master,name: None | str=None):
		children: list[customtkinter.CTkButton | TreeBranch] = []
		branch = TreeBranch(master,name)
		for key in tree.keys():
			data = tree[key]
			child = ""
			if (isinstance(data, str)):
				child = button(branch.children_frame,key)
				child.configure(command=lambda: self._handle(data))
			else:
				child = self.to_branch(data,branch.children_frame,key)
			branch.add_child(child)
		return branch

	def register_handler(self,func: Callable[[str]]):
		self.callables.append(func)

	def _handle(self,text: str):
		for func in self.callables:
			func(text)


class TreeBranch(customtkinter.CTkFrame):
	def __init__(self,
		master: customtkinter.CTkBaseClass,
		name: str | None,
	):
		super().__init__(master)
		#Lets leave column 0 and row 0 in case of any padding
		self.tree_children: list[customtkinter.CTkButton | TreeBranch] = []
		self.hidden = False
		self.row = 0
		if (name):
			self.name_butn = button(self,name,"expanded")
			self.name_butn.configure(command=lambda: self.toggle())
			self.name_butn.grid(column=1,row=1)
		else:
			self.name_butn = None
		self.children_frame = customtkinter.CTkFrame(self)
		self.children_frame.grid(column=1,row=2)
		self.children_frame.grid_columnconfigure(1, weight=1)
		self.children_frame.grid_columnconfigure(0, minsize=10)

	def add_child(self,child: customtkinter.CTkButton | TreeBranch):
		child.grid(
			column=1,
			row=self.row,
			# padx=(20,0),
			# pady=(20,0),
			sticky="ew"
		)
		self.row = self.row + 1
		self.tree_children.append(child)

	def toggle(self):
		self.hidden = not self.hidden
		self.apply()
		

	def hide(self):
		self.hidden = True
		self.apply()

	def show(self):
		self.hidden = False
		self.apply()

	def apply(self): 
		if (self.hidden):
			self.children_frame.grid_remove()
			if self.name_butn:
				self.name_butn.configure(image=button_closed)
		else: 
			self.children_frame.grid()
			if self.name_butn:
				self.name_butn.configure(image=button_open)
