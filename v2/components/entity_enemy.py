import glm
import random
import math

from utils.astar import astar

from components.entity import Entity

class Enemy(Entity):
	def __init__(
		self,
		renderer,
		terrain_component,
		obstacles_component,
	):
		super().__init__(renderer, terrain_component, obstacles_component)
		# setup states
		self.IDLE = 0
		self.WAITING = 1
		self.WALKING = 2
		self.state = self.IDLE
		# entity config
		self.radius = 4
		self.wait_time = 1000
		self.spawn_point = glm.vec3(8, 0, 8)
		self.obstacles = []
		for item in self.obstacles_component.obstacles_data:
			position = item['position']
			self.obstacles.append((position[0] - 0.5, position[2] - 0.5))
		# modify mesh
		self.reshape_entity()
		# register events
		self.update_method.append(self.simple_logic)

	def reshape_entity(self):
		self.geometry.position = self.spawn_point
		self.material.color = glm.vec3(1, 0, 0)

	def simple_logic(self, geometry, material):
		self.wait_time -= self.renderer.delta_time
		self.wait_time = max(0, self.wait_time)

		# generate random wait time when idle
		if self.state == self.IDLE:
			self.wait_time = random.uniform(2000, 5000)
			self.state = self.WAITING

		# generate walk path on wait time finish
		if self.state == self.WAITING and len(self.path) == 0 and self.wait_time == 0:
			# random angle and radius
			theta = random.uniform(0, 2 * math.pi)
			radius = random.uniform(0, self.radius)
			# radom point within radius
			x = self.spawn_point.x + radius * math.cos(theta)
			z = self.spawn_point.z + radius * math.sin(theta)

			start = (math.floor(geometry.position.x), math.floor(geometry.position.z))
			end = (math.floor(x), math.floor(z))

			self.path = astar([], start, end)
			self.state = self.WALKING

		# go back to idle when finished walking
		if self.state == self.WALKING and len(self.path) == 0:
			self.state = self.IDLE

