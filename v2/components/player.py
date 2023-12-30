import pygame
import glm
import math

from utils.lerp import lerp
from utils.astar import astar

from components.entity import Entity

class Player(Entity):
	def __init__(
		self,
		renderer,
		terrain_component,
		camera_component,
		obstacles_component,
	):
		super().__init__(renderer, terrain_component, camera_component)
		# setup obstacles for pathfinding
		self.obstacles_component = obstacles_component
		# register events
		self.register_events()

	def register_events(self):
		# move to projected target using a-star pathfind
		self.time_per_action = 500
		self.path = []
		self.target = None
		self.update_method.append(self.on_click)
		self.update_method.append(self.move_to_target)

	def move_to_target(self, geometry, material):
		if len(self.path) > 0:
			if self.renderer.elapsed_time % self.time_per_action > self.time_per_action - self.renderer.delta_time:
				target = self.path.pop(0)
				self.target = glm.vec3(target[0], 0, target[1])

		if self.target:
			geometry.position.x = lerp(geometry.position.x, self.target.x + 0.5, 0.05)
			geometry.position.z = lerp(geometry.position.z, self.target.z + 0.5, 0.05)

	def on_click(self, geometry, material):
		if pygame.mouse.get_pressed()[2] and len(self.path) == 0:
			intersection_point = self.get_intersection_point()

			obstacles = []
			for item in self.obstacles_component.obstacles_data:
				position = item['position']
				obstacles.append((position[0] - 0.5, position[2] - 0.5))
			start = (math.floor(geometry.position.x), math.floor(geometry.position.z))
			end = (math.floor(intersection_point.x), math.floor(intersection_point.z))

			self.path = astar(obstacles, start, end)

	def get_intersection_point(self):
		width = self.renderer.config['width']
		height = self.renderer.config['height']

		mouse_x, mouse_y = pygame.mouse.get_pos()

		near_point = glm.vec3(mouse_x, height - mouse_y, 0)
		far_point = glm.vec3(mouse_x, height - mouse_y, 1)

		near_world = glm.unProject(
			near_point,
			self.camera_component.m_view,
			self.camera_component.m_projection,
			(0, 0, width, height),
		)
		far_world = glm.unProject(
			far_point,
			self.camera_component.m_view,
			self.camera_component.m_projection,
			(0, 0, width, height),
		)
		ray_direction = glm.normalize(far_world - near_world)

		return self.ray_terrain_intersection(
			self.camera_component.position,
			ray_direction,
			self.terrain_component.geometry.height_map
		)

	def ray_terrain_intersection(self, ray_origin, ray_direction, height_map):
		plane_height = 0.0

		ray_direction = glm.normalize(ray_direction)
		t = (plane_height - ray_origin.y) / ray_direction.y
		intersection_point = ray_origin + t * ray_direction

		grid_x = int(intersection_point.x)
		grid_z = int(intersection_point.z)

		grid_x = max(0, min(grid_x, len(height_map[0]) - 1))
		grid_z = max(0, min(grid_z, len(height_map) - 1))

		intersection_point.y = height_map[grid_z][grid_x]

		return intersection_point
