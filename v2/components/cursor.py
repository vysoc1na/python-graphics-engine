import pygame
import math
import numpy
import glm

from utils.ray import ray
from utils.terrain_data import get_terrain_data

from core.geometry import PlaneGeometry
from core.material import SolidMaterial
from core.mesh import Mesh

from components.entity import Entity

class Cursor(Entity):
	def __init__(
		self,
		renderer,
		position,
		terrain_component,
		camera_component,
		obstacles_component,
	):
		super().__init__(renderer, terrain_component, obstacles_component)
		# save camera instance
		self.camera_instance = camera_component
		# register events
		self.update_method.append(self.on_mouse_move)
		# modify mesh
		self.reshape_entity()
		# store terrain corner positions
		self.corners = get_terrain_data(self.terrain_component.geometry.height_map)

	def reshape_entity(self):
		self.geometry = PlaneGeometry(
			position = (0, 1, 0),
			corners = (0, 0, 0, 0),
		)
		self.material = SolidMaterial(
			color = (0, 0, 1),
			transparency = 0.3,
		)
		self.mesh = Mesh(
			geometry = self.geometry,
			material = self.material,
			shader_program = self.renderer.shaders['default'],
			update_method = self.update_method,
		)

	def on_mouse_move(self, geometry, material):
		height_map = self.terrain_component.geometry.height_map
		# raycast position on terrain
		intersection_point = ray(
			self.renderer,
			self.camera_instance,
			height_map,
			pygame.mouse.get_pos(),
		)
		floor_x = math.floor(intersection_point.x)
		floor_z = math.floor(intersection_point.z)
		# find corners
		for item in self.corners:
			if item['position'].x == floor_z and item['position'].y == floor_x:
				geometry.corners = item['corners']
				# render new position and shape
				geometry.setup_vertex_data()
				geometry.position.x = math.floor(intersection_point.x) + 0.5
				geometry.position.y = 0.05
				geometry.position.z = math.floor(intersection_point.z) + 0.5
