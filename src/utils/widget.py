from collections import Counter
import customtkinter
import tkinter
def get_visible_children_count(container):
    visible_count = 0
    for child in container.winfo_children():
        if child.winfo_manager() != "":
            visible_count += 1
    return visible_count

def deep_count_elements(element):
    """
    Recursively counts all widgets nested inside 'element'.
    Returns a dictionary with specific breakdowns.
    """
    counts = Counter()
    def _recurse(current_node):
        # Gather all direct structural child elements
        children = current_node.winfo_children() 
        for child in children:
            # Determine if this component belongs to the CustomTkinter module
            module_name = type(child).__module__
            is_ctk = module_name.startswith("customtkinter")
            
            # Categorize the element type
            category = "CustomTkinter" if is_ctk else "Standard Tkinter"
            counts[category] += 1
            
            # Also track the exact class name for specific details (e.g., 'CTkButton' or 'Canvas')
            exact_class_name = type(child).__name__
            counts[f"{category} ({exact_class_name})"] += 1
            
            # Drill deeper into this child element's internal layout tree
            _recurse(child)
    _recurse(element)
    return dict(counts)
