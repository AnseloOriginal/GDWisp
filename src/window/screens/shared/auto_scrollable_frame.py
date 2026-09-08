import customtkinter

class AutoHidingScrollFrame(customtkinter.CTkScrollableFrame):

  def __init__(self, master: customtkinter.CTkBaseClass, **kwargs):
    self._scrollbar_visible = True
    super().__init__(master,**kwargs)
    self.bind("<Configure>", self.check_scrollbar, add="+")

  def check_scrollbar(self,event):
    self.update_idletasks()
    viewport_height = self._parent_canvas.winfo_height()
    content_height = self.winfo_reqheight()
    needs_scrollbar = content_height > viewport_height
    if needs_scrollbar == self._scrollbar_visible:
        return
    self._scrollbar_visible = needs_scrollbar
    if needs_scrollbar:
        self._scrollbar.grid()
    else:
        self._scrollbar.grid_remove()
