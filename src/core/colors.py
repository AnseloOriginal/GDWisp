from pathlib import Path
import customtkinter


def set_theme():
	SCRIPT_DIR = Path(__file__).parents[2]
	THEME_PATH = SCRIPT_DIR / "data" / "color-theme.json"
	customtkinter.set_default_color_theme(str(THEME_PATH))

main_frame = {
	"color": ["#FAFAFA","#313236"],
	"border_color": ["#586CA3","#575961"],
	"border_width": 1
}

#Used by custom widgets
theme_colors = {
	"butn_color": ("#D9D4FF", "#D9D4FF"),
    "hover_color": ("#BDB7FA", "#BDB7FA"),
    "border_color": ("#3E454A", "#949A9F"),
    "butn_text_color": ("#000000", "#000000"),
    "small_text_color": ("#103C7D", "#103C7D"),
}

#Used by the tree in Project view
tree_theme = {
	"text_color": ("#000000", "#FFFFFF"),
	"hover_color": ("#BDB7FA", "#BDB7FA")
}

#Used by difffing
standard_diff = {
	"frame_fg_color": ("#F2F7FF", "#F2F7FF"),
	"frame_border_color": ("#6B6B6B", "#6B6B6B"),
	"frame_border_width": 1,
	"old": "#960000",
	"new": "#007843"
}

status_colors = {
	"error": "#D32F2F",
	"success": "#2E7D32"
}

event_sheet = {
	"bg": ("#FFFAFA","#FFFAFA"),
	"icon": ("#FFFFFF","#FFFFFF"),
	"modified": ("#006699","#006699"),
	"added": ("#007843","#007843"),
	"removed": ("#960000","#960000"),
	"border": ("#000000","#000000"),
	"unmodified": ("#8C9BAE","#8C9BAE")
}