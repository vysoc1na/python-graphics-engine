class Scene():
	def __init__(self, renderer):
		# setup context
		self.renderer = renderer
		self.ctx = renderer.ctx
		# init children list
		self.children = []

	def render(self, camera):
		# render all children
		for item in self.children:
			item.render(
				projection = camera.m_projection,
				view = camera.m_view,
				ctx = self.ctx,
				render_mode = self.renderer.render_mode,
			)

	def destroy(self):
		# destroy all children
		for item in self.children:
			item.destroy()

	# TODO
	def check_event(self, event):
		# check for component events
		for item in self.children:
			item.check_event(event)
