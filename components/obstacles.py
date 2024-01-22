import glm

from core.geometry import BoxGeometry
from core.material import SolidMaterial
from core.mesh import MeshInstanced

class Obstacles():
	def __init__(
		self,
		renderer,
		terrain_component,
		obstacles_data,
	):
		self.renderer = renderer
		# setup terrain/obstacle data
		self.terrain_component = terrain_component
		self.obstacles_data = obstacles_data

		for item in obstacles_data:
			position = item['position']
			x = position[0]
			y = position[1]
			z = position[2]

			item['position'] = (x - 0.5, y, z - 0.5)

		# setup mesh
		self.on_init()

	def on_init(self):
		self.geometry = BoxGeometry(size = (1, 1.5, 1))
		self.material = SolidMaterial(
			color = (1, 0, 0),
			transparency = 0.2,
		)
		self.mesh = MeshInstanced(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['default'],
			instance_data = self.obstacles_data,
		)

