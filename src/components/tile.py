from mgl import ve3

class Tile():
	def __init__(self, app, mesh):
		self.app = app
		self.mesh = mesh

	def render(self):
		self.mesh.render()

	def destroy(self):
		self.mesh.destroy()

	def update(self, time):
		# fully rotate once every 5 seconds:
		self.mesh.rotation = vec3(0, time / 5000, 0)
		# update the mesh MVP to apply changes
		self.mesh.update()
