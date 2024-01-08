import math

from utils.noise import noise
from utils.color import brighten, saturate

from core.geometry import TerrainPlaneGeometry
from core.material import TerrainMaterial
from core.mesh import Mesh

class Terrain():
	def __init__(self, renderer):
		self.renderer = renderer
		# setup mesh
		self.on_init()

	def on_init(self):
		self.geometry = TerrainPlaneGeometry(
			position = (0.5, 0, 0.5),
			height_map = noise(64, 64, 8, 8, 0.2, 2, 0)
		)
		self.material = TerrainMaterial(
			color_low = saturate(brighten((0.45, 0.33, 0.16), 0.5), 1.5), # brown
			color_high = saturate((0.48, 0.65, 0.29), 1.5), # green
		)
		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['default'],
			# update_method = self.regenerate_terrain,
		)

	def regenerate_terrain(self, geometry, material):
		geometry.height_map = noise(16, 16, 4, 8, 0.2, 2, self.renderer.elapsed_time / 1000)
		geometry.setup_vertex_data()
