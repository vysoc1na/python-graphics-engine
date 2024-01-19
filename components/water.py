import glm

from core.geometry import BoxGeometry
from core.material import SolidMaterial
from core.mesh import Mesh

class Water():
	def __init__(
		self,
		renderer,
	):
		self.renderer = renderer

		# setup mesh
		self.on_init()

	def on_init(self):
		self.geometry = BoxGeometry(
			position = (32, -0.6, 32),
			size = (1, 1, 1),
			scale = (64, 1, 64),
		)
		self.material = SolidMaterial(
			color = (0, 1, 1),
			transparency = 0.2,
		)
		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['water'],
			update_method = self.set_elapsed_time_to_shader,
		)

	def set_elapsed_time_to_shader(self, geometry, material):
		self.mesh.shader_program['elapsed_time'] = self.renderer.elapsed_time
