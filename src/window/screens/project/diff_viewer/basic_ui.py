import customtkinter as CTk
from src.operations.git.diff.types import ActionType, BehaviourDiff, InstanceDiff, LayerDiff, ObjectGroupDiff, OldNewDiff, ResouceDiff, VariableDiff
from src.core.colors import standard_diff
from src.media.image import ICON

class DiffLine(CTk.CTkFrame):

    def __init__(self, master, name: str, oldText: str, newText: str, addColumn = True):
        super().__init__(master)
        self.grid_columnconfigure((1,3,5,7), minsize=10)
        bullet_image = CTk.CTkImage(light_image=ICON["bullet"], size=(10,10))
        bullet = CTk.CTkLabel(self, image=bullet_image, text="")
        bullet.grid(column=0, row=0,sticky="ew")
        labelText = name + ":" if addColumn else ""
        label = CTk.CTkLabel(self,text=labelText,anchor="w")
        new = CTk.CTkLabel(self,text=newText,text_color=standard_diff["new"],anchor="w")
        label.grid(column=2, row=0,sticky="ew")
        if (len(oldText) == 0):
            new.grid(column=4, row=0,sticky="ew")    
            return
        old = CTk.CTkLabel(self,text=oldText,text_color=standard_diff["old"],anchor="w")
        arrow_image = CTk.CTkImage(light_image=ICON["right arrow"])
        arrow = CTk.CTkLabel(self, image=arrow_image, text="")
        old.grid(column=4, row=0,sticky="ew")
        arrow.grid(column=6, row=0)
        new.grid(column=8, row=0, sticky="ew")

class ONDiffWidget(CTk.CTkFrame):

    def __init__(self, master, name: str, change: ActionType, diffs: list[OldNewDiff]) -> None:
        super().__init__(
            master,
            fg_color=standard_diff["frame_fg_color"],
            border_color=standard_diff["frame_border_color"],
            border_width=standard_diff["frame_border_width"]
        )

        self.columnconfigure(0, weight=1)

        frame = CTk.CTkFrame(self)
        frame.grid(column=0,row=0,sticky="ew",padx=20,pady=(10,0))
        frame.columnconfigure(1, weight=1)
        name_widget = CTk.CTkLabel(frame,text=name,anchor="w",font=(None, 14, "bold"))
        name_widget.grid(column=0,row=0,padx=(20,0))

        change_widget = CTk.CTkLabel(frame,text=change,anchor="w",font=(None, 12, "bold"))
        change_widget.grid(column=2,row=0,padx=(0,20))

        count = 1
        self.rowconfigure(1, minsize=10)
        for diff in diffs:
            line = DiffLine(
                self,diff["name"],
                str(diff["old"]),
                str(diff["new"]),
            )
            line.grid(column=0,row=count,sticky="ew",padx=20,pady=10)
            count += 1


class VarDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: VariableDiff) -> None:
        ondiff: list[OldNewDiff] = []

        if diff["var_type"]:
            ondiff.append(diff["var_type"])

        if diff["default"]:
            ondiff.append(diff["default"])

        super().__init__(
            master,
            diff["name"],
            diff["change"],
            ondiff
        )
        


class LayerDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: LayerDiff) -> None:
        super().__init__(
            master,
            diff["name"] if diff["name"] != "" else "Base Layer",
            diff["change"],
            diff["diff"] if diff["diff"] else []
        )


class InstanceDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: InstanceDiff) -> None:
        super().__init__(
            master,
            diff["display_name"],
            diff["change"],
            diff["diff"] if diff["diff"] else []
        )

class ObjectGroupDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: ObjectGroupDiff) -> None:
        super().__init__(
            master,
            diff["name"],
            diff["change"],
            [diff["diff"]] if diff["diff"] else []
        )

class BehaviourDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: BehaviourDiff) -> None:
        super().__init__(
            master,
            diff["name"],
            diff["change"],
            diff["diff"] if diff["diff"] else []
        )

class ResourceDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: ResouceDiff) -> None:
        super().__init__(
            master,
            diff["name"],
            diff["change"],
            diff["diff"] if diff["diff"] else []
        )

class EffectsDiffWidget(ONDiffWidget):

    def __init__(self, master, diff: ResouceDiff) -> None:
        super().__init__(
            master,
            diff["name"],
            diff["change"],
            diff["diff"] if diff["diff"] else []
        )