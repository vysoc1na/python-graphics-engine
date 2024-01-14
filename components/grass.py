import glm
import random
import math

from utils.color import saturate

from core.geometry import GrassBlade
from core.material import SolidMaterial
from core.mesh import Mesh

class Grass():
	def __init__(
		self,
		renderer,
		terrain_component,
		obstacles_component,
		position = (0, 0, 0),
		density = 50,
	):
		self.renderer = renderer
		self.terrain_component = terrain_component
		self.obstacles_component = obstacles_component

		self.spawn_point = glm.vec3(position) + glm.vec3(0.5, 0, 0.5)
		self.density = density

		blades_grid_data = []
		x = 0
		for row in self.terrain_component.geometry.height_map:
			x += 1
			z = 0
			for col in row:
				z += 1
				if col > 0:
					blades_grid_data.append({
						'position': (z, col, x)
					})

		self.blades_data = []
		for blade in blades_grid_data:
			position = blade['position']
			x = position[0] - 0.5
			y = position[1]
			z = position[2] - 0.5
			for density in range(math.floor(self.density * y)):
				offset = glm.vec3(random.uniform(0.1, 1.0) - 0.5, 0, random.uniform(0.1, 1.0) - 0.5)
				scale = random.uniform(y * 0.5, y * 1.5)
				self.blades_data.append({
					'position': glm.vec3(x, y, z) + offset,
					'scale': (scale, scale, scale),
				})

		self.on_init()

	def on_init(self):
		self.geometry = GrassBlade(data = self.blades_data)
		self.material = SolidMaterial(color = saturate((0.48, 0.65, 0.29), 1.5))
		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['grass'],
			update_method = self.set_elapsed_time_to_shader,
		)

	def set_elapsed_time_to_shader(self, geometry, material):
		self.mesh.shader_program['elapsed_time'] = self.renderer.elapsed_time

