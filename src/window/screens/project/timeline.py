import colorsys
import threading
import customtkinter
import tkinter as tk
from git import Commit
from queue import Queue
from time import perf_counter
from src.media.image import ICON
from src.core.colors import main_frame
from src.utils.colors import generate_unique_color
from typing import Literal, TypedDict, Callable
from src.operations.git.commit_manager import CommitManager



bullet = customtkinter.CTkImage(ICON["bullet"])
type ParentChildData = list[tuple[str,str]]
RESERVED_TOP_SPACES = 1000

type RefType = list[tuple[str, str]]
class ConsumedCommit:
	def __init__(self, commit: Commit):
		self.hexsha: str = commit.hexsha
		self.parents: list[str] = [parent.hexsha for parent in commit.parents]
		self.summary: str = str(commit.summary)
		self.author = commit.author.name or "Default"
		self.date = commit.authored_date
		self.date_tz = commit.author_tz_offset
		self.action: Literal["Commit", "Merge", "Branch Point"] = "Commit"

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
		self.commit_list: dict[str, ConsumedCommit] = {}
		self.grid_columnconfigure((0,4),minsize=5)
		self.grid_columnconfigure(2,minsize=10)
		self.grid_columnconfigure((1,3),weight=1)
		self.grid_rowconfigure(1,weight=1)
		self.grid_rowconfigure((0,2),minsize=5)
		self.path = repo_path
		self.queue = Queue()
		self.ext_funcs: None | Callable[[str, ConsumedCommit | bool],None] = None
		self.processed: int = 0
		self.no_of_commits: None | int = None
		self._parent_canvas.configure(yscrollcommand=self.check_scroll)
		self.used_bottom_spaces = 0
		self.used_top_spaces = 0

		self.text_frame = customtkinter.CTkFrame(self)
		self.lines: dict[str, BranchLine] = {}
		self.new_lines: dict[str, BranchLine] = {}
		self.scanvas = BranchDrawingEngine(self,repo_path,self.on_click,width=100)
		self.text_frame.grid(row=1,column=3,sticky="nsew")
		self.scanvas.grid(column=1,row=1, sticky="nsew")
		first_thread = threading.Thread(target=self.update_info)
		self.running_thread = True
		self.running_top_thread = False
		first_thread.start()
		
	def update_info(self,is_top=False):
		start = perf_counter()
		commits_manager = CommitManager(self.path)
		if self.no_of_commits is None:
			self.no_of_commits = commits_manager.no_of_commits()
		if is_top:
			raw_commits = commits_manager.commits(0,max=10)
		else:
			raw_commits = commits_manager.commits(self.processed)
		commits = [ConsumedCommit(commit) for commit in raw_commits]
		refs = commits_manager.get_refs()
		evt: InfoEventType = {
			"commits": commits,
			"refs": refs
		}
		end = perf_counter() - start
		print(f"Timeline update took {end}s to complete")
		self.queue.put(evt)
		self.after(0, self.update_ui, is_top)

	def update_ui(self, is_top: bool):
		print("[UI Update]")
		data: InfoEventType = self.queue.get(block=False)
		commits = data["commits"]
		for commit in commits[:]:
			if not is_top:
				break
			line_exists = self.lines.get(commit.hexsha,False)
			if line_exists:
				commits.remove(commit)
		self.put_texts(commits,is_top)
		# Only call after put_texts has updated lines
		self.build_nodes(data["refs"],is_top)
		#Do the end of thread here to ensure if only updates after build
		if is_top:
			self.running_top_thread = False
		else:
			self.running_thread = False

	def put_texts(self, commits: list[ConsumedCommit], above: bool = False): 
		self.commit_list |= {commit.hexsha: commit for commit in commits}
		self.processed += len(commits)
		self.new_lines = {}
		for commit in commits:
			#Skip RESERVED_TOP_SPACES  
			top = (RESERVED_TOP_SPACES - self.used_top_spaces -1)
			bottom = (RESERVED_TOP_SPACES + self.used_bottom_spaces + 1)
			n = top if above else bottom
			index = commit.hexsha
			line = BranchLine(self.text_frame,commit,n)
			line.configure(command=lambda id=index: self.on_click(id))
			self.lines[index] = line
			self.new_lines[index] = line
			line.grid(row=n,column=3, pady=5, sticky="nswe")
			if above:
				self.used_top_spaces += 1
			else:
				self.used_bottom_spaces += 1
		
	def build_nodes(self,refs: RefType, is_top=False):
		if len(self.new_lines) == 0:
			return
		self.scanvas.build(
			self.new_lines,
			refs,
			self.lines,
			is_top
		)

	def on_click(self, hexsha: str):
		commit = self.commit_list.get(hexsha, None)
		if (not commit):
			return
		if (not self.ext_funcs):
			return
		commit.action = self.scanvas.commit_type(hexsha)
		self.ext_funcs(hexsha, commit)

	def check_new_commits(self):
		if self.running_top_thread:
			return False
		self.running_top_thread = True
		top_update_thread = threading.Thread(target=self.update_info, args=[True])
		top_update_thread.start()


	def clear(self):
		for id,line in self.lines.items():
			line.destroy()
		self.processed = 0
		self.no_of_commits = None
		self.used_bottom_spaces = 0
		self.used_top_spaces = 0
		self.lines = {}
		self.new_lines= {}
		# Do not clear any thread booleans

	def refresh(self):
		self.clear()
		self.scanvas.clear()
		self.running_thread = True
		if self.ext_funcs:
			self.ext_funcs("",True)
		self._parent_canvas.yview_moveto(0)
		threading.Thread(target=self.update_info).start()
		
	def check_scroll(self,top, bottom):
		self._scrollbar.set(top,bottom)
		top, bottom = self._parent_canvas.yview()
		not_finished = self.no_of_commits is not None and self.processed < self.no_of_commits
		should_start = not self.running_thread and not_finished
		if bottom > 0.99 and should_start:
			print("Loading new data")
			update_thread = threading.Thread(target=self.update_info)
			self.running_thread = True
			update_thread.start()




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
		self, 
		parent,repo_path: str, onclick: Callable[[str], None],
		width=100, **kwargs
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
		self.master_merge_list: list[str] = []
		self.master_branching_list: list[str] = []
		self.future_commit_list: list[str] = []
		self.future_branching_list: ParentChildData = []
		self.future_merge_list: ParentChildData = []
		self.all_lines = {}
		self.circle_data: dict[str, tuple[float, float, str]] =  {}
		self.onclick=onclick


	def center_x(self):
		return self.width/2

	def get_center(self,line: BranchLine):
		w = line.winfo_width()
		h = line.winfo_height()
		x = line.winfo_x()
		y = line.winfo_y()
		return x+(w/2), y+(h/2)

	def create_circle(self, x, y, r, color="black"):
		return self.create_oval(x-r, y-r, x+r, y+r, fill=color, tags="current")

	def modify_circle(self,id, x, y, r, color: str | None = None):
		self.coords(id, [x-r, y-r, x+r, y+r])

	def is_ref_of(self,hexsha: str):
		for ref in self.refs:
			if ref[0] == hexsha:
				return ref[1]
		return False

	def create_branch(self,branch_name:str,hexsha: str):
		existing_branch = self.branches.get(branch_name,None)
		if existing_branch:
			existing_branch.add_parent(hexsha)
		else:
			count = len(self.branches)
			lane = -40 + (len(self.branches) * 20)
			branch = Branch(lane,color=generate_unique_color(count+1))
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

	def branch_of(self,hexsha: str):
		for name,branch in self.branches.items():
			if branch.has_child(hexsha):
				return branch
		return None

	def children_of(self,hexsha: str):
		children: list[str] = []
		for name,branch in self.branches.items():
			child = branch.child_of(hexsha)
			if child:
				children.append(child)
		return children

	def remove_from_branches(self,hexsha: str, target_branch: str | None = None):
		parents: list[str] = []
		for name,branch in self.branches.items():
			if target_branch is not None and target_branch != name:
				continue
			parent = branch.remove_child(hexsha)
			if parent:
				parents.append(parent)
		return parents

	def commit_type(self,hexsha: str):
		if hexsha in self.master_merge_list:
			return "Merge"
		if hexsha in self.master_branching_list:
			return "Branch Point"
		return "Commit"

	def is_future_commit(self,*hexshas, use_list: dict[str, BranchLine] | None = None):
		checklist = use_list if use_list else self.all_lines
		ret = False
		for hexsha in hexshas:
			exists = checklist.get(hexsha, None)
			if exists is None:
				return True
		return ret


	def build(self,
		lines: dict[str,BranchLine],
		refs: RefType,
		all_lines: dict[str,BranchLine],
		is_top: bool = False
	):
		self.all_lines = all_lines
		circles = []
		self.refs = refs
		self.master.update_idletasks()
		self.update_idletasks()
		merge_list: ParentChildData = []
		branching_list: ParentChildData = []

		for hexsha, line in lines.items():
			print("Processing",line.id)
			is_root = len(line.commit.parents) == 0
			is_tip = self.is_ref_of(line.id) # This returns the branch name
			is_merge = len(line.commit.parents) > 1
			one_child = len(line.commit.parents) ==  1

			if one_child:
				parent_exists = self.exists_in_branch(line.commit.parents[0])
			else:
				parent_exists = False

			if is_tip:
				exists_in_other_branch = self.exists_in_branch(line.id)
				if (exists_in_other_branch):
					parents = self.remove_from_branches(line.id,exists_in_other_branch)
					for child in parents:
						print("Remove parent",line.id," from ",exists_in_other_branch," and merge to",child)
						merge_list.append((child,line.id))
				print("Found new branch: ",is_tip," Commit: ",line.id)
				self.create_branch(is_tip,line.id)

			if is_merge:
				print("Found merge",line.commit.parents)
				self.master_merge_list.append(line.id)
				self.add_to_branch(line.id,line.commit.parents[0])
				second_parent = line.commit.parents[1]
				if not self.exists_in_branch(second_parent):
					name = f"Lane for {second_parent}"
					self.create_branch(name,second_parent)
				merge_list.append((line.id,line.commit.parents[1]))

			if one_child:
				if parent_exists:
					# Branching point due to parent existing in another branch
					children = self.children_of(line.commit.parents[0])
					children.append(line.id)
					print("Children:",children)
					for child in children:
						print(f"Found that {line.commit.parents[0]} branched out to {child}")
						self.master_branching_list.append(line.commit.parents[0])
						branching_list.append((child,line.commit.parents[0]))
				else:
					self.add_to_branch(line.id,line.commit.parents[0])
			print(" ")
			print(" ")

		self.draw_main_branch_line(lines)
		self.draw_connecting_line("branch",branching_list)
		self.draw_connecting_line("merge",merge_list)
		self.draw_connecting_line("fbranch",self.future_branching_list)
		self.draw_connecting_line("fmerge",self.future_merge_list)
		self.draw_circles_for(lines)
		if is_top:
			self.adjust_top_area(lines)

	def adjust_top_area(self, lines: dict[str, BranchLine]):
		self.update_idletasks()
		accomodation = 0
		extraspace = 0 #need due to the fact that circle is at center
		for hexsha, line in lines.items():
			pady = line.grid_info().get("pady",0)
			if not isinstance(pady,int):
				pady = pady[0] + pady[1]
			else:
				pady = pady * 2
			extraspace = line.winfo_height()/2
			height = line.winfo_height()
			final_value = height + pady
			accomodation += height
		print("Accomodating",accomodation,len(lines))
		x1, y1, x2, y2 = self.bbox("all")
		self.configure(scrollregion=(x1, y1 - extraspace, x2, y2))
		self.yview_scroll(int(accomodation), "units")
	
	def draw_connecting_line(
		self,
		line_type: Literal["branch", "merge", "fbranch", "fmerge"],
		process_list: ParentChildData,
	):
		to_be_removed: ParentChildData = []
		for data in process_list:
			child, parent = data
			if self.is_future_commit(child,parent):
				if line_type == "branch":
					self.future_branching_list.append(data)
				elif line_type == "merge":
					self.future_merge_list.append(data)
				continue
			cx, cy, ccolor  = self.circle_data[child]
			px, py, pcolor = self.circle_data[parent]
			self.create_line(cx,cy,px,py, fill=ccolor)
			to_be_removed.append(data)
		for data in to_be_removed:
			if line_type == "fbranch":
				self.future_branching_list.remove(data)
			elif line_type == "fmerge":
				self.future_merge_list.remove(data)

	def draw_main_branch_line(self,lines: dict[str, BranchLine]):
		center_x = self.center_x()
		for hexsha, line in lines.items():
			branch = self.branch_of(hexsha)
			if not branch:
				print("Line",line.id,"has not branch")
				continue
			lane =  branch.lane
			color = branch.color
			parent = branch.parent_of(hexsha)
			x,y = self.get_center(line)
			cx, cy = (center_x+lane, y)
			self.circle_data[line.id] = (cx,cy,color)
			if parent:
				px,py,color = self.circle_data[parent]
				self.create_line(cx,cy,px,py, fill=color)

	def draw_circles_for(self,lines: dict[str, BranchLine]):
		for hexsha, line in lines.items():
			data =  self.circle_data.get(hexsha, None)
			if not data:
				continue
			cx, cy, color = data
			circle = self.create_circle(cx,cy,5, color=color)

			def handle_click(evt, cx=cx, cy=cy, i=circle, hexsha=hexsha):
				self.modify_circle(i, cx, cy, 6)
				self.onclick(hexsha)
				self.after(100, self.modify_circle, i, cx, cy, 7)

			self.tag_bind(circle, "<Button-1>", handle_click)
			self.tag_bind(circle, "<Enter>", 
				lambda evt, cx=cx, cy=cy, i=circle: self.modify_circle(i,cx,cy,7))
			self.tag_bind(circle, "<Leave>", 
				lambda evt, cx=cx, cy=cy, i=circle: self.modify_circle(i,cx,cy,5))

	def clear(self):
		self.delete("all")
		self.branches = {}
		self.refs = []
		self.master_merge_list = []
		self.master_branching_list = []
		self.future_commit_list = []
		self.future_branching_list = []
		self.future_merge_list = []
		self.all_lines = {}
		self.circle_data = {}

class Branch:
	def __init__(self, lane: int, color: str="black") -> None:
		self.list: list[str] = []
		self.color = color
		self.lane = lane
		#For speed we maintain an equal set
		self.fast_set = set(self.list)


	def add_child(self,hexsha: str):
		if not self.has_child(hexsha):
			self.list.insert(0,hexsha)
			self.fast_set.add(hexsha)

	def add_parent(self,hexsha: str):
		if not self.has_child(hexsha):
			self.list.append(hexsha)
			self.fast_set.add(hexsha)

	def has_child(self,hexsha: str):
		if hexsha in self.fast_set:
			return True
		else:
			return False

	def remove_child(self,hexsha: str):
		"""Removes a child and returns its parent if it exists"""
		if self.has_child(hexsha):
			index = self.list.index(hexsha)
			self.list.remove(hexsha)
			self.fast_set.discard(hexsha)
			parent = False if index == 0 else self.list[index-1]
			return parent
		else:
			return False

	def parent_of(self,hexsha: str):
		if self.has_child(hexsha):
			child_index = self.list.index(hexsha)
			last_index = len(self.fast_set)-1
			if child_index == last_index:
				return None
			return self.list[child_index+1]
		else:
			return None

	def child_of(self,hexsha: str):
		if self.has_child(hexsha):
			child_index = self.list.index(hexsha)
			next_index = child_index+1
			print("DEBUG",child_index,next_index)
			if next_index < len(self.fast_set):
				return self.list[next_index]
			return None
		else:
			return None
