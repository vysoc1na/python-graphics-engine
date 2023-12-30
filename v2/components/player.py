import pygame
import glm
import math

from utils.lerp import lerp

from components.entity import Entity

class Player(Entity):
	def __init__(self, renderer, terrain_component, camera_component):
		super().__init__(renderer, terrain_component, camera_component)
		# register events
		self.register_events()

	def register_events(self):
		# move staight line to projected target from mouse coordinates
		self.is_clicked = False
		self.target = None
		self.update_method.append(self.on_click)
		self.update_method.append(self.move_to_target)
		# TODO a* pathfinding with obstacles

	def move_to_target(self, geometry, material):
		if self.target and self.is_clicked == True:
			smoothness = 0.05

			geometry.position.x = lerp(geometry.position.x, self.target.x, smoothness)
			geometry.position.z = lerp(geometry.position.z, self.target.z, smoothness)

			if abs(self.target.x - geometry.position.x) < smoothness:
				if abs(self.target.z - geometry.position.z) < smoothness:
					self.is_clicked = False
					self.target = None

	def on_click(self, geometry, material):
		if pygame.mouse.get_pressed()[2] and self.is_clicked == False:
			self.is_clicked = True

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
			intersection_point = self.ray_terrain_intersection(
				self.camera_component.position,
				ray_direction,
				self.terrain_component.geometry.height_map
			)

			self.target = glm.vec3(
				math.floor(intersection_point.x) + 0.5,
				intersection_point.y,
				math.floor(intersection_point.z) + 0.5,
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
