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
		position,
		terrain_component,
		camera_component,
		obstacles_component,
	):
		super().__init__(renderer, terrain_component, obstacles_component, camera_component)
		# entity config
		self.spawn_point = glm.vec3(position) + glm.vec3(0.5, 0, 0.5)
		# modify mesh
		self.reshape_entity()
		# register events
		self.update_method.append(self.on_click)
		self.update_method.append(self.change_color_on_action)

	def reshape_entity(self):
		self.geometry.position = self.spawn_point

	def change_color_on_action(self, geometry, material):
		if len(self.path):
			material.color = glm.vec3(0, 0, 1)
		else:
			material.color = glm.vec3(1, 1, 0)

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

		m_view = self.camera_component.m_view
		m_projection = self.camera_component.m_projection
		viewport = (0, 0, width, height)

		near_world = glm.unProject(near_point, m_view, m_projection, viewport)
		far_world = glm.unProject(far_point, m_view, m_projection, viewport)
		ray_direction = glm.normalize(far_world - near_world)

		return ray(
			self.camera_component.position,
			ray_direction,
			self.terrain_component.geometry.height_map
		)
