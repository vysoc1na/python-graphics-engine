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
			intersection_point = ray(
				self.renderer,
				self.camera_component,
				self.terrain_component.geometry.height_map,
				pygame.mouse.get_pos(),
			)

			start = (math.floor(geometry.position.x), math.floor(geometry.position.z))
			end = (math.floor(intersection_point.x), math.floor(intersection_point.z))

			self.path = astar(self.obstacles, start, end)
