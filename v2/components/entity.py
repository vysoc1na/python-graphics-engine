import glm
import math

from utils.interpolate import interpolate
from utils.lerp import lerp

from core.geometry import BoxGeometry
from core.material import SolidMaterial
from core.mesh import Mesh

class Entity():
	def __init__(
		self,
		renderer,
		terrain_component,
		obstacles_component,
		camera_component = None,
	):
		self.renderer = renderer
		self.terrain_component = terrain_component
		self.camera_component = camera_component
		# setup obstacles for pathfinding
		self.obstacles_component = obstacles_component
		self.obstacles = []
		for item in self.obstacles_component.obstacles_data:
			position = item['position']
			self.obstacles.append((position[0] - 0.5, position[2] - 0.5))
		# update methods
		self.update_method = []
		# setup mesh
		self.on_init()

	def on_init(self):
		self.geometry = BoxGeometry(size = (0.1, 0.5, 0.1), position = (0.5, 0, 0.5))
		self.material = SolidMaterial(color = (1, 1, 1))
		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['default'],
			update_method = self.update_method,
		)

		# move along path of x-z coordinates
		self.time_per_action = 500
		self.path = []
		self.target = None
		self.update_method.append(self.move_to_target)
		# snap entity to terrain
		self.update_method.append(self.snap_to_terrain)
		# only follow entities with attached camera component
		if self.camera_component:
			self.update_method.append(self.snap_camera)

	def move_to_target(self, geometry, material):
		if len(self.path) > 0:
			if self.renderer.elapsed_time % self.time_per_action > self.time_per_action - self.renderer.delta_time:
				target = self.path.pop(0)
				self.target = glm.vec3(target[0], 0, target[1])

		if self.target:
			geometry.position.x = lerp(geometry.position.x, self.target.x + 0.5, 0.05)
			geometry.position.z = lerp(geometry.position.z, self.target.z + 0.5, 0.05)

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

	def snap_camera(self, geometry, material):
		radius = max(1, self.camera_component.position.y)
		angle = math.radians(self.camera_component.yaw - 180)

		target_x = geometry.position.x + radius * math.cos(angle)
		target_z = geometry.position.z + radius * math.sin(angle)

		self.camera_component.position.x = target_x
		self.camera_component.position.z = target_z

		self.camera_component.m_view = glm.lookAt(
			self.camera_component.position,
			geometry.position + self.camera_component.up,
			self.camera_component.up,
		)
