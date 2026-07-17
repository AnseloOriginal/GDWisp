import customtkinter as CTk
from queue import Queue
import threading
from git import Commit
from src.operations.git.tools import get_commit
import tkinter.font as tkfont

from src.operations.project.tools import diff_from_commit

class ConsumedCommit:
	def __init__(self, commit: Commit):
		self.message = str(commit.message)
		self.author = commit.author.name or "Default"
		self.date = commit.authored_date
		self.date_tz = commit.author_tz_offset

class GrowingProgressBar(CTk.CTkFrame):
	def __init__(self, parent, **kwargs):
		super().__init__(parent)
		bar = CTk.CTkProgressBar(self, **kwargs, width=100)
		self.grid_columnconfigure((0,2),weight=1)
		self.grid_rowconfigure((0,2),weight=1)
		bar.grid(column=1,row=1)
		self.bar = bar


class CommitExtraInfo(CTk.CTkToplevel):

	def __init__(self, parent, location: str, hexsha: str):
		super().__init__(parent)
		self.title("Extra Commit Info")
		self.grab_set()
		self.geometry("400x500")
		thread1 = threading.Thread(target=self.commit_data)
		thread2 = threading.Thread(target=self.engine_data)
		self.commit_queue = Queue()
		self.engine_queue = Queue()
		self.location = location
		self.hexsha = hexsha
		self.scroll = CTk.CTkScrollableFrame(self)
		self.scroll.grid(column=0,row=0,sticky="nsew")
		self.grid_rowconfigure(0,weight=1)
		self.grid_columnconfigure(0,weight=1)
		self._ui_setup()
		thread1.start()
		thread2.start()


	def _ui_setup(self):
		self.scroll.grid_columnconfigure(0,weight=1)
		progressbar = GrowingProgressBar(self.scroll, 
			orientation="horizontal",mode="indeterminate")
		progressbar.grid(column=0,row=0,sticky="ew",pady=50)
		progressbar.bar.start()
		self.p1 = progressbar
		specific_title = CTk.CTkLabel(
							self.scroll,
							text="Engine-Specific Changes",
							anchor="w",
							font=(None,12,"bold")
		)
		specific_title.grid(column=0,row=1,sticky="ew",padx=(5,0))
		progressbar2 = GrowingProgressBar(self.scroll, 
			orientation="horizontal",mode="indeterminate")
		progressbar2.grid(column=0,row=2,sticky="ew",pady=50)
		progressbar2.bar.start()
		self.p2 = progressbar2


	def commit_data(self):
		raw_commit = get_commit(self.location,self.hexsha)
		commit = ConsumedCommit(raw_commit)
		self.commit_queue.put(commit, block=False)
		self.after(0, self._ui_commit_data)

	def engine_data(self):
		diff =  diff_from_commit(self.location,self.hexsha)
		diff_strs = diff.data_as_str() if diff else []  
		self.engine_queue.put(diff_strs, block=False)
		self.after(0, self._ui_engine_data)

	def _ui_engine_data(self):
		diffs: list[str] = self.engine_queue.get(block=False)
		if type(diffs) is not list:
			diffs = []
		self.p2.grid_forget()
		body  = CTk.CTkFrame(self.scroll)
		body.grid_columnconfigure(0,weight=1)
		body.grid(column=0,row=2,sticky="nswe")
		header_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
		textbox = CTk.CTkTextbox(body,height=200)
		for data in diffs:
			textbox.insert("end", f"\n-{data}")
		if len(diffs) == 0:
			textbox.insert("1.0", f"\n{"We couldn't find any difference."}")
		textbox.configure(state="disabled")
		textbox.grid(column=0,row=0, sticky="ew", padx=10)

	def _ui_commit_data(self):
		commit: ConsumedCommit = self.commit_queue.get(block=False)
		if type(commit) is not ConsumedCommit:
			return
		self.p1.grid_forget()
		body  = CTk.CTkFrame(self.scroll)
		body.grid_columnconfigure(0,weight=1)
		body.grid(column=0,row=0,sticky="nswe")
		header_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
		textbox = CTk.CTkTextbox(body,height=200)
		textbox._textbox.tag_config("header", font=header_font)
		# textbox.tag_config("header", font=(None, None, "bold"))
		textbox.insert("1.0", "Commit Message:\n","header")
		textbox.insert("end", commit.message)
		textbox.insert("end", "\n\nFull Hexsha: ","header")
		textbox.insert("end", self.hexsha)
		textbox.configure(state="disabled")
		textbox.grid(column=0,row=0, sticky="ew", padx=10)

		

