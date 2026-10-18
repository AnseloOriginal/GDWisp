from __future__ import annotations
from math import floor
import customtkinter
import time
from types import NoneType
from typing import Literal
from src.utils.list import safe_get
from src.utils.widget import deep_count_elements, get_visible_children_count
from src.operations.git.diff.main import Diff
from src.core.colors import standard_diff
from src.operations.git.diff.types import SceneDiff
from src.window.screens.project.diff_viewer.events_ui import UNMODIFIED, create_event_widget
from src.window.screens.shared.auto_scrollable_frame import AutoHidingScrollFrame
from src.window.screens.project.diff_viewer.basic_ui import BehaviourDiffWidget, DiffLine, EffectsDiffWidget, InstanceDiffWidget, LayerDiffWidget, ObjectGroupDiffWidget, ResourceDiffWidget, VarDiffWidget
from src.window.screens.project.diff_viewer.event_pocket import EventPocket
import cProfile, pstats


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
        elif newview == "resources":
            self._render_resources()
        elif newview.startswith("scene::"):
            parts = newview.split("::")
            self._render_scene(parts[1],parts[2],parts[3:])
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
            old = self.to_string(props["old"])
            new = self.to_string(props["new"])
            diff = DiffLine(area,props["name"],old,new)
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

    def _render_resources(self):
        self.apply_fix(True)
        self.wipe()
        if (not self.diff or not self.diff.resourcesDiff):
            return
        
        area = self.area_centered_helper(True,True)
        self.default_heading_helper(self,"Project Resources")
        count = 1
        for diff in self.diff.resourcesDiff:
            widget = ResourceDiffWidget(area,diff)
            widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
            count = count + 1

    def _render_scene(self,scene_name: str, component: str, extras: list = []):
        self.apply_fix(True)
        self.wipe()
        if not self.diff:
            return
        scene = self.diff.scene_diffs.get(scene_name)
        if not scene:
            return
        if component == "properties":
            self._render_scene_properties(scene,scene_name)
        elif component == "variables":
            self._render_scene_variables(scene,scene_name)
        elif component == "layers":
            self._render_scene_layers(scene,scene_name)
        elif component == "instances":
            self._render_scene_instances(scene,scene_name)
        elif component == "object_groups":
            self._render_scene_object_groups(scene,scene_name)
        elif component == "object":
            index = int(safe_get(extras,0,False))
            print("Safety:",index)
            if isinstance(index,bool):
                return
            print("Safety:",index)
            self._render_object("scene",index,scene)
        elif component == "ui":
            self._render_scene_ui(scene,scene_name)
        elif component == "events":
            self._render_scene_events(scene,scene_name)

    def _render_object(self, source: Literal["scene", "global"], index: int, scene: SceneDiff | None = None):
        diff = None
        if source == "scene" and scene:
            objs = scene.get("objects")
            diff = safe_get(objs,index) if objs else None

        if not diff:
            return

        area = self.area_centered_helper(True,True)
        self.default_heading_helper(self,f"{diff["name"]} {diff["uuid"][:6]} - Scene Object ({diff["change"]})")

        count = 3
        if diff["variables"]:
            self.mini_heading_helper(area,"Object Variables",count,1)
            count += 1
            for var in diff["variables"]:
                widget = VarDiffWidget(area,var)
                widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
                count += 1

        if diff["behaviours"]:
            self.mini_heading_helper(area,"Object Behaviours",count,1)
            count += 1
            for behaviour in diff["behaviours"]:
                widget = BehaviourDiffWidget(area,behaviour)
                widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
                count += 1

        if diff["effects"]:
            self.mini_heading_helper(area,"Object Effects",count,1)
            count += 1
            for effect in diff["effects"]:
                widget = EffectsDiffWidget(area,effect)
                widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
                count += 1

    def _render_scene_variables(self, scene: SceneDiff, name: str):
        var = scene.get("variables")
        if not var:
            return
        area = self.area_centered_helper(True,True)
        self.default_heading_helper(self,f"{name} Variables")

        count = 1
        for diff in var:
            widget = VarDiffWidget(area,diff)
            widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
            count = count + 1

    def _render_scene_properties(self, scene: SceneDiff, name: str):
        area = self.area_centered_helper()
        self.default_heading_helper(area,f"{name}  -  Scene Properties")
        props = scene.get("properties")
        if not props:
            return
        count = 1
        for prop in props:
            line = DiffLine(area,
                prop["name"],
                self.to_string(prop["old"]),
                self.to_string(prop["new"])
            )
            line.grid(row=count,column=1, sticky="ew")
            count = count + 1

    def _render_scene_ui(self, scene: SceneDiff, name: str):
        area = self.area_centered_helper()
        self.default_heading_helper(area,f"{name}  -  Editor UI Settings")
        ui = scene.get("ui")
        if not ui:
            return
        count = 1
        for prop in ui:
            line = DiffLine(area,
                prop["name"],
                self.to_string(prop["old"]),
                self.to_string(prop["new"])
            )
            line.grid(row=count,column=1, sticky="ew")
            count = count + 1

    def _render_scene_layers(self, scene: SceneDiff, name: str):
        area = self.area_centered_helper(True,True)
        self.default_heading_helper(area,f"{name}  -  Scene Layers")
        layers = scene.get("layers")
        if not layers:
            return
        count = 1
        for layer in layers:
            widget = LayerDiffWidget(area,layer)
            widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
            count += 1

    def _render_scene_object_groups(self, scene: SceneDiff, name: str):
        area = self.area_centered_helper(True,True)
        self.default_heading_helper(area,f"{name}  -  Scene Object Groups")
        groups = scene.get("object_groups")
        if not groups:
            return
        count = 1
        for group in groups:
            widget = ObjectGroupDiffWidget(area,group)
            widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
            count += 1

    def _render_scene_instances(self, scene: SceneDiff, name: str):
        area = self.area_centered_helper(True,True)
        self.default_heading_helper(area,f"{name}  -  Scene Instances")
        instances = scene.get("instances")
        if not instances:
            return
        count = 1
        for instance in instances:
            widget = InstanceDiffWidget(area,instance)
            widget.grid(row=count,column=1, pady=20, padx=10,sticky="ew")
            count += 1


    def area_centered_helper(self, transparent: bool = False, expand: bool = False, autogrid: bool = True):
        area = self.create_content_area(transparent)
        if autogrid:
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

    def mini_heading_helper(self,parent,text: str, row: int=0, column: int=0):
        heading = customtkinter.CTkLabel(
            parent,text=text,font=(None, 14, "bold"),anchor="nw"
        )
        heading.grid(column=column,row=row, sticky="ew", pady=5)
        return heading

    def to_string(
            self,obj
        ):
        obj_type = type(obj)
        if (obj_type == str):
            return f'"{obj}"'
        elif(obj_type == int or obj_type == bool or obj_type == float):
            return str(obj)
        elif (type(obj) == NoneType):
            return ""
        elif (type(obj) == list):
            return str(obj)
        else:
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

    def _render_scene_events(self, scene: SceneDiff, name: str):
        area = self.area_centered_helper(True,True,False)
        self.default_heading_helper(area,f"{name}  -  Scene Events")
        event_store = scene.get("events")
        meta = self.diff.metadata_scanner if self.diff else None
        if not event_store or not meta:
            return
        count = 1
        context_count = 0
        current_pocket: None | EventPocket = None
        def batch_widget_grid(time: int, widget, row: int):
            self.after(
                time,
                lambda: widget.grid(row=row,column=1, pady=5, padx=10,sticky="ew")
            )
        start_time = time.perf_counter()
        # profiler.enable()
        for event in event_store:
            widget =  create_event_widget(area,event,meta)
            queue_time = floor(count / 10) * 500
            if not widget:
                continue
            if widget.flag == UNMODIFIED:
                if context_count < 2:
                    context_count += 1
                    # widget.grid(row=count,column=1, pady=5, padx=10,sticky="ew")
                    batch_widget_grid(queue_time,widget,count)
                else:
                    if current_pocket is None:
                        current_pocket = EventPocket(area,bg_color="black")
                        batch_widget_grid(queue_time,widget,count)
                        count += 1
                    # Must happen before adding to pocket for checks
                    batch_widget_grid(queue_time,widget,count)
                    current_pocket.add(widget)
                count += 1
            else:    
                batch_widget_grid(queue_time,widget,count)
                count += 1
                context_count = 0
                current_pocket = None
        area.grid(column=1,row=1,sticky="nsew")
        # area.update_idletasks()
        # profiler.disable()
        end_time = time.perf_counter()
        # stats = pstats.Stats(profiler).sort_stats("tottime")
        # stats.print_stats(15) 
        print(f"""The event rendering took {end_time - start_time}s with  
            {get_visible_children_count(area)-1} visible events, {len(event_store)} events in total""")
        print(f"Deep count of elements: {deep_count_elements(area)}")

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