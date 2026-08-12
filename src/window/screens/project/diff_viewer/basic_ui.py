import customtkinter as CTk
from src.operations.git.diff.types import LayerDiff, VariableDiff
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


class VarDiffWidget(CTk.CTkFrame):

    def __init__(self, master, diff: VariableDiff) -> None:
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

        name = CTk.CTkLabel(frame,text=diff["name"],anchor="w",font=(None, 14, "bold"))
        name.grid(column=0,row=0,padx=(20,0))

        change = CTk.CTkLabel(frame,text=diff["change"],anchor="w",font=(None, 12, "bold"))
        change.grid(column=2,row=0,padx=(0,20))

        if diff["var_type"]:
            var_type_line = DiffLine(
                self,diff["var_type"]["name"],
                str(diff["var_type"]["old"]),
                str(diff["var_type"]["new"]),
            )
            var_type_line.grid(column=0,row=2,sticky="ew",padx=20,pady=10)

        if diff["default"]:
            default_value_line = DiffLine(
                self,diff["default"]["name"],
                str(diff["default"]["old"]),
                str(diff["default"]["new"]),
            )
            default_value_line.grid(column=0,row=3,sticky="ew",padx=20,pady=10)


class LayerDiffWidget(CTk.CTkFrame):

    def __init__(self, master, diff: LayerDiff) -> None:
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
        displayName = diff["name"] if diff["name"] != "" else "Base Layer"
        name = CTk.CTkLabel(frame,text=displayName,anchor="w",font=(None, 14, "bold"))
        name.grid(column=0,row=0,padx=(20,0))

        change = CTk.CTkLabel(frame,text=diff["change"],anchor="w",font=(None, 12, "bold"))
        change.grid(column=2,row=0,padx=(0,20))

        count = 1
        prop_diff = diff["diff"]
        if not prop_diff:
            return
        for prop in prop_diff:
            line = DiffLine(
                self,prop["name"],
                str(prop["old"]),
                str(prop["new"]),
            )
            line.grid(column=0,row=count,sticky="ew",padx=20,pady=10)
            count += 1
