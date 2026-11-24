from typing import Any, Callable, TypedDict
from customtkinter import CTkScrollbar, CTkBaseClass
from threading import Timer

type ScrollItem = tuple[CTkBaseClass | Callable[[],CTkBaseClass], int, int, dict[str, Any]]

class RenderQueueItem(TypedDict):
	widget: CTkBaseClass
	row: int
	column: int
	extras: dict

class LazyScroller:

	def __init__(self, scrollbar: CTkScrollbar, max_item: int) -> None:
		self.scrollbar = scrollbar
		self.old_scroll_function: Callable | None = self.scrollbar._command or None
		self.scrollbar.configure(command=self.manage_scroll)
		self.master_list: dict[int, ScrollItem] = {}
		self.debounce_timer: None | Timer = None
		self.processed_widgets = set()
		self.max_item = max_item
		self.render_queue: list[RenderQueueItem] = []

	def add(self, widget: CTkBaseClass | Callable[[],CTkBaseClass], row: int, column: int, **extras):
		item: ScrollItem = (widget,row,column,extras)
		self.master_list[row] = item
		if len(self.processed_widgets) < self.max_item:
			self.process_item(item)
		self.process_render_queue()

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
				self.process_item(item)
				item_count += 1
		self.process_render_queue()

	def process_item(self, item: ScrollItem):
		widget, row, column, extras = item
		if isinstance(widget,Callable):
			widget = widget()
		self.processed_widgets.add(row)
		queue_item = RenderQueueItem(widget=widget,row=row,column=column,extras=extras)
		self.render_queue.append(queue_item)

	def process_render_queue(self):
		for item in self.render_queue:
			item["widget"].grid(
				row=item["row"],column=item["column"],
				**item["extras"]
			)
		self.render_queue = []






