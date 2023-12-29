from utils.noise import noise

from core.geometry import TerrainPlaneGeometry
from core.material import SolidMaterial
from core.mesh import Mesh

class Terrain():
	def __init__(self, renderer):
		self.renderer = renderer
		# setup mesh
		self.on_init()

	def on_init(self):
		self.geometry = TerrainPlaneGeometry(
			position = (0.5, 0, 0.5),
			height_map = noise(16, 16, 4, 8, 0.2, 2, 0)
		)
		self.material = SolidMaterial(color = (0.2, 0.3, 0.2))
		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['default'],
			update_method = [
				self.regenerate_terrain,
			]
		)

	def regenerate_terrain(self, geometry, material):
		geometry.height_map = noise(16, 16, 4, 8, 0.2, 2, self.renderer.elapsed_time / 1000)
		geometry.setup_vertex_data()
