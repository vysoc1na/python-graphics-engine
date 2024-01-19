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
		logger = None,
	):
		self.logger = logger
		super().__init__(renderer, terrain_component, obstacles_component, camera_component)
		# entity config
		self.spawn_point = glm.vec3(position) + glm.vec3(0.5, 0, 0.5)
		# modify mesh
		self.reshape_entity()
		# register events
		self.is_clicked = False
		self.clicked_time = 0
		self.update_method.append(self.on_click)
		self.update_method.append(self.change_color_on_action)

	def reshape_entity(self):
		self.geometry.position = self.spawn_point
		self.material.color = glm.vec3(0, 0, 1)

	def change_color_on_action(self, geometry, material):
		if len(self.path) > 0:
			color_state = glm.vec3(0, 0.5, 1)
		else:
			color_state = glm.vec3(0, 0, 1)

		if glm.length(material.color - color_state) > 0:
			material.color = color_state
			self.mesh.should_update = True

	def on_click(self, geometry, material):
		if self.is_clicked == True:
			if self.renderer.elapsed_time > self.clicked_time + 500:
				self.is_clicked = False
			return

		if pygame.mouse.get_pressed()[2] and len(self.path) == 0:
			self.is_clicked = True
			self.clicked_time = self.renderer.elapsed_time

			intersection_point = ray(
				self.renderer,
				self.camera_component,
				self.terrain_component.geometry.height_map,
				pygame.mouse.get_pos(),
			)

			start = (math.floor(geometry.position.x), math.floor(geometry.position.z))
			end = (math.floor(intersection_point.x), math.floor(intersection_point.z))

			self.path = astar(self.obstacles, start, end)

			if end in self.obstacles and self.logger != None:
				self.logger.add(f'cannot move "player" to obstacle at {end}')

			if len(self.path) > 0 and self.logger != None:
				self.logger.add(f'moving "player" from {start} to {end}')
