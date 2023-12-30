import pygame
import glm
import math

from utils.lerp import lerp
from utils.astar import astar
from utils.ray import ray

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
		self.obstacles = []
		for item in self.obstacles_component.obstacles_data:
			position = item['position']
			self.obstacles.append((position[0] - 0.5, position[2] - 0.5))
		# register events
		self.update_method.append(self.on_click)

	def on_click(self, geometry, material):
		if pygame.mouse.get_pressed()[2] and len(self.path) == 0:
			intersection_point = self.get_intersection_point()

			start = (math.floor(geometry.position.x), math.floor(geometry.position.z))
			end = (math.floor(intersection_point.x), math.floor(intersection_point.z))

			self.path = astar(self.obstacles, start, end)

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

		return ray(
			self.camera_component.position,
			ray_direction,
			self.terrain_component.geometry.height_map
		)
