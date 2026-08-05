from __future__ import annotations
from types import NoneType
from typing import Literal
import customtkinter
from git import diff
from src.core.colors import standard_diff, main_frame
from src.media.image import ICON
from src.operations.git.diff import Diff
from src.window.screens.shared.helpers import AutoHidingScrollFrame
from src.window.screens.shared.conversion import properties_name
from src.window.screens.project.diff_viewer.basic_ui import DiffLine, VarDiffWidget

class ProjectViewDiff(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkBaseClass, diff: Diff | None, parent: customtkinter.CTkTabview | None =None):
        super().__init__(master)
        self.diff = diff
        self.grid_columnconfigure((0,2),minsize=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure((0,2),minsize=20)
        self.parent = parent
        self.current_view = "placeholder"
        self._render_placeholder()

    def wipe(self):
        for child in self.winfo_children():
            child.destroy()
        self.update_idletasks()

    def _render_placeholder(self):
        self.apply_fix(False)
        self.wipe()
        text = customtkinter.CTkLabel(self,text="Look at the left panel to see changes")
        text.grid(column=1,row=1,sticky="nsew")

    def change_view(self,newview: str):
        if newview == "properties":
            self._render_properties()
        elif newview == "placeholder":
            self._render_placeholder()
        elif newview == "globalvar":
            self._render_globalvar()
        else:
            self._render_placeholder()
        self.current_view = newview

    def _render_properties(self):
        self.apply_fix(True)
        self.wipe()
        if (not self.diff or not self.diff.propertiesDiff):
            return

        area = self.area_centered_helper()
        self.default_heading_helper(area,"Project Properties")
        count = 1
        for props in self.diff.propertiesDiff:
            label = self.to_string(props["name"], "properties")
            old = self.to_string(props["old"],"force")
            new = self.to_string(props["new"],"force")
            diff = DiffLine(area,label,old,new)
            diff.grid(row=count,column=1, sticky="ew")
            count = count + 1

    def _render_globalvar(self):
        self.apply_fix(True)
        self.wipe()
        if (not self.diff or not self.diff.globalVarDiff):
            return
        
        area = self.area_centered_helper(True,True)
        self.default_heading_helper(self,"Global Variables")
        count = 1
        for diff in self.diff.globalVarDiff:
            widget = VarDiffWidget(area,diff)
            widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
            count = count + 1


    def area_centered_helper(self, transparent: bool = False, expand: bool = False):
        area = self.create_content_area(transparent)
        area.grid(column=1,row=1,sticky="nsew")
        if expand:
            area.grid_columnconfigure(1,weight=1)
            area.grid_columnconfigure((0,2),minsize=20)
        else:
            area.grid_columnconfigure(0,minsize=20)
        return area

    def default_heading_helper(self,parent,text: str):
        heading = customtkinter.CTkLabel(
            parent,text=text,font=(None, 18, "bold"),anchor="nw"
        )
        heading.grid(column=1,row=0, sticky="ew", pady=20)
        return heading



    def to_string(
            self,obj, 
            conv_type1: Literal["properties","force"], 
            conv_type2: Literal["none"] = "none"
        ):
        if conv_type1 == "properties":
            return properties_name.get(obj, "Unknown")
        elif conv_type1 == "force":
            obj_type = type(obj)
            if (obj_type == str):
                return '"'+obj+'"'
            elif(obj_type == int or obj_type == bool):
                return str(obj)
            elif (type(obj) == NoneType):
                return ""
            elif (type(obj) == list):
                return str(obj)
            else:
                print(obj,type(obj))
                return "[COMPLEX]"

    def create_content_area(self,transparent: bool):
        color = standard_diff["frame_fg_color"] if (not transparent) else "transparent"
        focus = customtkinter.CTkFrame(
            self,
            height=500,
            fg_color=color,
            border_color=standard_diff["frame_border_color"],
            border_width=standard_diff["frame_border_width"] if not transparent else 0,
        )
        focus.grid_columnconfigure((0,2), minsize=5)
        focus.grid_rowconfigure((0,2), minsize=5)
        focus.grid_columnconfigure(1, weight=1)
        focus.grid_rowconfigure(1, weight=1)
        focus.grid(column=1,row=1,sticky="news")
        scroll = AutoHidingScrollFrame(focus,
                fg_color=color
        )
        return scroll

    def apply_fix(self,shouldApply: bool):
        if (not self.parent):
            return
        if (shouldApply):
            self.parent.grid_rowconfigure(0, minsize=0, weight=0)
        else:
            self.parent.grid_rowconfigure(0, weight=0, 
                minsize=self.parent._apply_widget_scaling(self.parent._outer_spacing)
            )
    def refresh(self):
        if self.current_view == "placeholder":
            return
        self.change_view(self.current_view)