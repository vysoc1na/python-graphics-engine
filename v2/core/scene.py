class Scene():
	def __init__(self, renderer):
		# setup context
		self.renderer = renderer
		self.ctx = renderer.ctx
		# init children list
		self.children = []

	def render(self):
		# render all children
		for item in self.children:
			item.render()

	def destroy(self):
		# destroy all children
		for item in self.children:
			item.destroy()

	def check_event(self, event):
		# check for component events
		for item in self.children:
			item.check_event(event)
