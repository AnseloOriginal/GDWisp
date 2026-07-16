from __future__ import annotations
from queue import Queue
from threading import Thread
from typing import Literal, Callable
import customtkinter
from src.media.image import ICON
from src.core.colors import tree_theme
from src.operations.git.diff import Diff
from src.operations.project.diff_related import project_diff
from src.window.views.project_view_helpers.extrainfo import GrowingProgressBar


type TreeStructure = dict[str, TreeStructure | str]
type on_click_func = Callable[[str]]
type on_update_func = Callable[[Diff]]

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

	def __init__(self, master, location: str, folder: str):
		super().__init__(master)
		self.on_clicks: list[on_click_func] = []
		self.on_updates :list[on_update_func] = []
		self.location = location
		self.folder = folder
		self.update_queue = Queue()
		self.mainFrame: None | TreeBranch = None
		self.diff: None | Diff = None
		self.loading = GrowingProgressBar(self,mode="indeterminate")
		self.update_thread = Thread(target=self.update_tree)
		self.update_thread.start()
		self.running = True
		self.no_change = False
		self.reset()
		self.trigger_rerun = False

	def render(self):
		self.reset() #To make sure its deleted
		diff: Diff = self.update_queue.get(False)
		if type(diff) is not Diff:
			return
		if self.trigger_rerun:
			self.refresh()
			return
		self.diff = diff
		self._handle_update(diff)
		no_change = not diff.changes_exists()
		self.no_change = no_change
		if no_change:
			text="No Changes Found"
			notext = customtkinter.CTkLabel(self,font=(None,12,"bold"),text=text)
			notext.grid(column=0,row=0)
			return
		self.grid_columnconfigure(0, weight=0)
		self.grid_rowconfigure(0, weight=0)
		tree = generate_tree_data(diff)
		self.mainFrame = self.to_branch(tree,self)
		self.mainFrame.grid(column=0, row=0)
		

	def update_tree(self):
		diff = project_diff(self.location,self.folder)
		self.update_queue.put(diff, block=False)
		self.running = False
		self.after(0, self.render)

	def reset(self):
		if self.mainFrame:
			self.mainFrame.destroy()
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)
		self.loading.grid(column=0, row=0, sticky="nsew",pady=20)
		self.loading.bar.start()

	def to_branch(self,tree: TreeStructure,master,name: None | str=None):
		children: list[customtkinter.CTkButton | TreeBranch] = []
		branch = TreeBranch(master,name)
		for key in tree.keys():
			data = tree[key]
			child = ""
			if (isinstance(data, str)):
				child = button(branch.children_frame,key)
				child.configure(command=lambda: self._handle_click(data))
			else:
				child = self.to_branch(data,branch.children_frame,key)
			branch.add_child(child)
		return branch

	def register_click_handler(self,func: on_click_func):
		self.on_clicks.append(func)

	def register_update_handler(self,func: on_update_func):
		self.on_updates.append(func)


	def _handle_click(self,text: str):
		for func in self.on_clicks:
			func(text)

	def _handle_update(self,diff: Diff):
		for func in self.on_updates:
			func(diff)

	def refresh(self):
		if self.running:
			self.trigger_rerun = True
		else:
			self.update_thread = Thread(target=self.update_tree)
			self.update_thread.start()
			self.trigger_rerun = False			


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



def generate_tree_data(diff: "Diff"): 
  data: TreeStructure = {}
  if (diff.propertiesDiff != None):
    if (data.get("Project", None) == None):
      data["Project"] = {}
    data["Project"]["Properties"] = "properties"
  return data