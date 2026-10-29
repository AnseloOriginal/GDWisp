from typing import Any, Callable
from customtkinter import CTkScrollbar, CTkBaseClass
from threading import Timer

type ScrollItem = tuple[CTkBaseClass | Callable[[],CTkBaseClass], int, int, dict[str, Any]]

class LazyScroller:

	def __init__(self, scrollbar: CTkScrollbar, max_item: int) -> None:
		self.scrollbar = scrollbar
		self.old_scroll_function: Callable | None = self.scrollbar._command or None
		self.scrollbar.configure(command=self.manage_scroll)
		self.master_list: dict[int, ScrollItem] = {}
		self.debounce_timer: None | Timer = None
		self.processed_widgets = set()
		self.max_item = max_item

	def add(self, widget: CTkBaseClass | Callable[[],CTkBaseClass], row: int, column: int, **extras):
		item: ScrollItem = (widget,row,column,extras)
		self.master_list[row] = item
		if len(self.processed_widgets) < self.max_item:
			self.place_item(item)
			self.processed_widgets.add(row)

	def manage_scroll(self, *kwargs):
		if self.old_scroll_function:
			self.old_scroll_function(*kwargs)
		top, bottom = self.scrollbar.get()
		if bottom >= 0.99:
			self.debounce_scroll()

	def debounce_scroll(self):
		if self.debounce_timer:
			self.debounce_timer.cancel()
		self.debounce_timer = Timer(0.5,self.fill_bottom)
		self.debounce_timer.start()

	def fill_bottom(self):
		item_count = 0
		for row, item in self.master_list.items():
			if item_count >= self.max_item:
				break 
			if row in self.processed_widgets:
				continue
			else:
				self.place_item(item)
				self.processed_widgets.add(row)
				item_count += 1

	def place_item(self, item: ScrollItem):
		widget, row, column, extras = item
		if isinstance(widget,Callable):
			widget = widget()
		widget.grid(row=row,column=column,**extras)





