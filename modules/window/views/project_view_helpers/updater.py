from modules.window.views.project_view_helpers.timeline import Timeline
from modules.window.views.project_view_helpers.tree import Tree, generate_tree_data

class Updater:

	def __init__(self, timeline: Timeline, tree: Tree):
		self.timeline = timeline
		self.tree = tree
		pass

	def trigger(self):
		pass
