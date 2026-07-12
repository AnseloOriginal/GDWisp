from __future__ import annotations
from types import NoneType
from typing import Literal
import customtkinter
from git import diff
from modules.config.colors import standard_diff
from modules.media.image import ICON
from modules.operations.git.diff import Diff
from modules.window.views.helpers import AutoHidingScrollFrame
from modules.window.views.conversion import properties_name

class DiffLine(customtkinter.CTkFrame):

    def __init__(self, master, name: str, oldText: str, newText: str, addColumn = True):
        super().__init__(master)
        self.grid_columnconfigure((1,3,5,7), minsize=10)
        bullet_image = customtkinter.CTkImage(light_image=ICON["bullet"], size=(10,10))
        bullet = customtkinter.CTkLabel(self, image=bullet_image, text="")
        bullet.grid(column=0, row=0,sticky="ew")
        labelText = name + ":" if addColumn else ""
        label = customtkinter.CTkLabel(self,text=labelText,anchor="w")
        new = customtkinter.CTkLabel(self,text=newText,text_color=standard_diff["new"],anchor="w")
        label.grid(column=2, row=0,sticky="ew")
        if (len(oldText) == 0):
            new.grid(column=4, row=0,sticky="ew")    
            return
        old = customtkinter.CTkLabel(self,text=oldText,text_color=standard_diff["old"],anchor="w")
        arrow_image = customtkinter.CTkImage(light_image=ICON["right arrow"])
        arrow = customtkinter.CTkLabel(self, image=arrow_image, text="")
        old.grid(column=4, row=0,sticky="ew")
        arrow.grid(column=6, row=0)
        new.grid(column=8, row=0, sticky="ew")

class ProjectViewDiff(customtkinter.CTkFrame):
    def __init__(self, master: customtkinter.CTkBaseClass, diff: Diff | None, parent: customtkinter.CTkTabview | None =None):
        super().__init__(master)
        self.diff = diff
        self.grid_columnconfigure((0,2),minsize=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure((0,2),minsize=20)
        self.parent = parent
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
        if (newview == "properties"):
            self._render_properties()
        elif newview == "placeholder":
            self._render_placeholder()

    def _render_properties(self):
        self.apply_fix(True)
        self.wipe()
        if (not self.diff or not self.diff.propertiesDiff):
            return

        area = self.create_content_area()
        area.grid(column=1,row=1,sticky="nsew")
        area.grid_columnconfigure(0,minsize=20)
        heading = customtkinter.CTkLabel(area,text="Project Properties",font=(None, 18, "bold"),anchor="nw")
        heading.grid(column=1,row=0, sticky="ew", pady=20)
        count = 1
        for props in self.diff.propertiesDiff:
            label = self.to_string(props["name"], "properties")
            old = self.to_string(props["old"],"force")
            new = self.to_string(props["new"],"force")
            diff = DiffLine(area,label,old,new)
            diff.grid(row=count,column=1, sticky="ew")
            count = count + 1

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

    def create_content_area(self):
        pass
        focus = customtkinter.CTkFrame(
            self,
            height=500,
            fg_color=standard_diff["frame_fg_color"],
            border_color=standard_diff["frame_border_color"],
            border_width=standard_diff["frame_border_width"],
        )
        focus.grid_columnconfigure((0,2), minsize=5)
        focus.grid_rowconfigure((0,2), minsize=5)
        focus.grid_columnconfigure(1, weight=1)
        focus.grid_rowconfigure(1, weight=1)
        focus.grid(column=1,row=1,sticky="news")
        scroll = AutoHidingScrollFrame(focus,
                fg_color=standard_diff["frame_fg_color"]
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