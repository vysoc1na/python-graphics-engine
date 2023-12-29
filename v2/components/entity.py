import glm
import math

from utils.interpolate import interpolate

from core.geometry import BoxGeometry
from core.material import SolidMaterial
from core.mesh import Mesh

class Entity():
	def __init__(self, renderer, terrain_component):
		self.renderer = renderer
		self.terrain_component = terrain_component
		# setup mesh
		self.on_init()

	def on_init(self):
		self.geometry = BoxGeometry(size = (0.1, 0.5, 0.1))
		self.material = SolidMaterial(color = (0.8, 0.6, 0.2))

		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['default'],
			update_method = [
				self.move_around_circle,
				self.snap_to_terrain,
			],
		)

	def move_around_circle(self, geometry, material):
		new_position = glm.vec3(geometry.position)
		# move on circle
		new_position.x = math.sin(self.renderer.elapsed_time / 3000) * 5 + 8
		new_position.z = math.cos(self.renderer.elapsed_time / 3000) * 5 + 8
		# set new position to geometry
		geometry.position = new_position

	def snap_to_terrain(self, geometry, material):
		new_position = glm.vec3(geometry.position)
		height_map = self.terrain_component.geometry.height_map
		x, y, z = geometry.position
		# indexes and relative posiitons
		floor_x, floor_z = math.floor(x), math.floor(z)
		frac_x, frac_z = x - floor_x, z - floor_z
		# check if point is inside of terrain bounds
		if floor_z > len(height_map) - 2 or floor_x > len(height_map[0]) - 2:
			return
		if floor_z < 0 or floor_x < 0:
			return
		# get corner heights
		top_left = height_map[floor_z][floor_x]
		top_right = height_map[floor_z][floor_x + 1]
		bottom_left = height_map[floor_z + 1][floor_x]
		bottom_right = height_map[floor_z + 1][floor_x + 1]
		# interpolat throught all 4 corners
		top_interpolated = interpolate(top_left, top_right, frac_x)
		bottom_interpolated = interpolate(bottom_left, bottom_right, frac_x)
		interpolated_height = interpolate(top_interpolated, bottom_interpolated, frac_z)
		# setup new Y component
		new_position.y = interpolated_height + (geometry.size.y / 2)
		# assign new position
		geometry.position = new_position
