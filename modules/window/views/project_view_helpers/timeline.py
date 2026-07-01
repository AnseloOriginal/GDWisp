import queue
from time import perf_counter
from git.exc import BadObject
from git.objects import commit
from git import Commit
from modules.window.views.helpers import AutoHidingScrollFrame
from modules.operations.git.tools import commit_list
from modules.operations.git.helpers import CommitHelper
from collections.abc import Iterator
import customtkinter
from typing import TypedDict
from modules.media.image import ICON
from queue import Queue
import threading
import tkinter as tk
from modules.config.colors import main_frame

bullet = customtkinter.CTkImage(ICON["bullet"])

type RefType = list[tuple[str, str]]
class ConsumedCommit:
	def __init__(self, commit: Commit):
		self.hexsha: str = commit.hexsha
		self.parents: list[str] = [parent.hexsha for parent in commit.parents]
		self.summary: str = str(commit.summary)

class InfoEventType(TypedDict):
	refs: RefType
	commits: list[ConsumedCommit]

class Timeline(customtkinter.CTkScrollableFrame):
	def __init__(
		self, 
		master: customtkinter.CTkBaseClass,
		repo_path: str,
		 **kwargs
	):
		super().__init__(master, width=350,height=500,**kwargs)
		self.grid_columnconfigure((0,4),minsize=5)
		self.grid_columnconfigure(2,minsize=10)
		self.grid_columnconfigure((1,3),weight=1)
		self.grid_rowconfigure(1,weight=1)
		self.grid_rowconfigure((0,2),minsize=5)
		self.path = repo_path
		self.queue = Queue()

		self.text_frame = customtkinter.CTkFrame(self)
		self.lines: list[BranchLine] = []
		self.scanvas = BranchDrawingEngine(self,repo_path,width=100)
		
		self.text_frame.grid(row=1,column=3,sticky="nsew")
		self.scanvas.grid(column=1,row=1, sticky="nsew")
		first_thread = threading.Thread(target=self.update_info)
		# self.scanvas.bind("<<UpdateInfoComplete>>",lambda evt: self.update_ui())
		first_thread.start()
		
	def update_info(self):
		start = perf_counter()
		helper = CommitHelper(self.path)
		raw_commits = helper.commits()
		commits = [ConsumedCommit(commit) for commit in raw_commits]
		refs = helper.get_refs()
		evt: InfoEventType = {
			"commits": commits,
			"refs": refs
		}
		end = perf_counter() - start
		print(f"Timeline update took {end}s to complete")
		self.queue.put(evt)
		self.after(0, self.update_ui)

	def update_ui(self):
		print("[UI Update]")
		data: InfoEventType = self.queue.get(block=False)
		self.put_texts(data["commits"])
		# Only call after put_texts has updated lines
		self.build_nodes(data["refs"])

	def put_texts(self, commits: list[ConsumedCommit]):
		n = 0
		for commit in commits:
			index = commit.hexsha
			line = BranchLine(self.text_frame,commit,n)
			self.lines.append(line)
			line.grid(row=n,column=3, pady=5, sticky="nswe")
			n = n + 1
		
	def build_nodes(self,refs: RefType):
		if len(self.lines) == 0:
			return
		self.scanvas.build(
			self.lines,
			refs
		)


class Dot(customtkinter.CTkButton):

	def __init__(self,parent):
		super().__init__(
			parent,
			bg_color="transparent",
			fg_color="transparent",
			text="",
			image=bullet,
			width=30
		)



class BranchLine(customtkinter.CTkButton):
	def __init__(self,parent,commit: ConsumedCommit, n: int):
		super().__init__(parent,text=commit.summary,anchor="w",fg_color="transparent")
		self.id = commit.hexsha
		self.commit = commit
		self.n = n

class BranchDrawingEngine(tk.Canvas):
	def __init__(
		self, parent,repo_path: str,width=100,**kwargs
		):
		super().__init__(
			parent,
			width=100,
			**kwargs,
			bg=main_frame["color"][0],
			borderwidth=0,
			border=0
		)
		self.width = width
		self.repo_path = repo_path
		self.branches: dict[str, Branch] = {}
		self.refs = []

	def center_x(self):
		return self.width/2

	def get_center(self,line: BranchLine):
		w = line.winfo_width()
		h = line.winfo_height()
		x = line.winfo_x()
		y = line.winfo_y()
		return x+(w/2), y+(h/2)

	def create_circle(self, x, y, r, color="black"):
		return self.create_oval(x-r, y-r, x+r, y+r, fill=color)

	def is_ref_of(self,hexsha: str):
		for ref in self.refs:
			if ref[0] == hexsha:
				return ref[1]
		return False

	def create_branch(self,branch_name:str,hexsha: str):
		color_list = [
			"orange", "blue", "purple",
			"red", "yellow"
		]
		count = len(self.branches)
		branch = Branch(color=color_list[count])
		branch.add_child(hexsha)
		self.branches[branch_name] = branch

	def add_to_branch(self,descendant: str, hexsha: str):
		for name,branch in self.branches.items():
			if branch.has_child(descendant):
				branch.add_child(hexsha)
				print(f"Added commit {hexsha} after {descendant} in Branch {name}")
				return
	def exists_in_branch(self,hexsha: str):
		for name,branch in self.branches.items():
			if branch.has_child(hexsha):
				return name
		return False

	def remove_from_branches(self,hexsha: str):
		parents: list[str] = []
		for name,branch in self.branches.items():
			parent = branch.remove_child(hexsha)
			if parent:
				parents.append(parent)
		return parents

	def build(self,
		lines: list[BranchLine],
		refs: RefType
	):
		print(refs)
		circle_data: dict[str, tuple[float, float, str]] =  {}
		circles = []
		line_map: dict[str, BranchLine] =  {}
		self.refs = refs
		self.master.update_idletasks()
		self.update_idletasks()
		center_x = self.center_x()
		merge_list: list[tuple[str,str]] = []
		branching_list: list[tuple[str,str]] = []

		for line in lines:
			print("Processing",line.id)
			is_root = len(line.commit.parents) == 0
			is_tip = self.is_ref_of(line.id) # This returns the branch name
			is_merge = len(line.commit.parents) > 1
			one_child = len(line.commit.parents) ==  1

			if (is_tip):
				exists_in_other_branch = self.exists_in_branch(line.id)
				if (exists_in_other_branch):
					parents = self.remove_from_branches(line.id)
					for child in parents:
						merge_list.append((child,line.id))
				print("Found new branch: ",is_tip," Commit: ",line.id)
				self.create_branch(is_tip,line.id)

			if (is_merge):
				print("Found merge",line.commit.parents)
				self.add_to_branch(line.id,line.commit.parents[0])
				merge_list.append((line.id,line.commit.parents[1]))

			if (one_child):
				parent_exists = self.exists_in_branch(line.commit.parents[0])
				if (parent_exists):
					# Branching point due to multiple exists
					print(f"Found that {line.commit.parents[0]} branched out to {line.id}")
					branching_list.append((line.id,line.commit.parents[0]))
				else:
					self.add_to_branch(line.id,line.commit.parents[0])
			line_map[line.id] = line
			print(" ")
			print(" ")
			
		dist = 0 if len(self.branches) == 1 else (len(self.branches)-2)*-30
		for name,branch in self.branches.items():
			last_hexsha = None
			color = branch.color
			for hexsha in branch.list:
				line = line_map[hexsha]
				x,y = self.get_center(line)
				cx, cy = (center_x+dist, y)
				circle_data[line.id] = (cx,cy,color)
				if (last_hexsha):
					px,py,color = circle_data[last_hexsha]
					self.create_line(cx,cy,px,py, fill=color)
				last_hexsha = hexsha
			dist += 30

		for child, parent in branching_list:
			cx, cy, ccolor  = circle_data[child]
			px, py, pcolor = circle_data[parent]
			self.create_line(cx,cy,px,py, fill=ccolor)

		for child, parent in merge_list:
			cx, cy, ccolor = circle_data[child]
			px, py, pcolor = circle_data[parent]
			self.create_line(cx,cy,px,py, fill=pcolor)

		for hexsha,data in circle_data.items():
			cx, cy, color = data
			circle = self.create_circle(cx,cy,5, color=color)
		

class Branch:
	def __init__(self,color: str="black") -> None:
		self.list: list[str] = []
		self.color = color

	def add_child(self,hexsha: str):
		if not hexsha in self.list:
			self.list.insert(0,hexsha)

	def has_child(self,hexsha: str):
		return self.list.count(hexsha) > 0

	def remove_child(self,hexsha: str):
		"""Removes a child and returns its parent if it exists"""
		if self.has_child(hexsha):
			index = self.list.index(hexsha)
			self.list.remove(hexsha)
			parent = False if index == 0 else self.list[index-1]
			return parent
		else:
			return False


