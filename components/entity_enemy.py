import glm
import random
import math

from utils.astar import astar

from components.entity import Entity

class Enemy(Entity):
	def __init__(
		self,
		renderer,
		position,
		terrain_component,
		obstacles_component,
		logger = None,
		name = 'enemy',
		walk_radius = 16,
		wait_time = (5000, 10000),
		ressurect_time = 5000,
		health = 10,
	):
		self.logger = logger
		self.name = name
		super().__init__(renderer, terrain_component, obstacles_component)
		# setup states
		self.IDLE = 0
		self.WAITING = 1
		self.WALKING = 2
		self.DEAD = 3
		self.WAITING_DEAD = 4
		self.state = self.DEAD
		# entity config
		self.radius = walk_radius
		self.wait_time_options = wait_time
		self.wait_time = ressurect_time
		self.ressurect_time = ressurect_time
		self.spawn_point = glm.vec3(position) + glm.vec3(0.5, 0, 0.5)
		self.spawn_health = health
		# entity state
		self.health = health
		self.take_damage = 0
		# modify mesh
		self.reshape_entity()
		# register events
		self.update_method.append(self.simple_logic)
		self.update_method.append(self.change_color_on_action)

	def reshape_entity(self):
		self.geometry.position = self.spawn_point
		self.material.color = glm.vec3(1, 0, 0)

	def change_color_on_action(self, geometry, material):
		color_state = material.color
		size_state = geometry.size
		rotate_state = geometry.rotation

		if self.state == self.DEAD or self.state == self.WAITING_DEAD:
			color_state = glm.vec3(0.5, 0.5, 0.5)
			size_state = glm.vec3(0.5, 0.1, 0.1)
			rotate_state = glm.vec3(0, 45, 0)
		else:
			size_state = glm.vec3(0.1, 0.5, 0.1)
			rotate_state = glm.vec3(0, 0, 0)
			if len(self.path):
				color_state = glm.vec3(1, 0.5, 0)
			else:
				color_state = glm.vec3(1, 0, 0)

		if glm.length(geometry.size - size_state) > 0:
			geometry.size = size_state
			geometry.rotation = rotate_state
			geometry.update_vertices()

		if glm.length(material.color - color_state) > 0:
			material.color = color_state
			self.mesh.should_update = True

	def simple_logic(self, geometry, material):
		self.wait_time -= self.renderer.delta_time
		self.wait_time = max(0, self.wait_time)

		# take damage or die
		if self.health > 0 and self.take_damage > 0:
			self.health = max(0, self.health - self.take_damage)
			self.take_damage = 0

			if self.logger != None:
				self.logger.add(f'dealing damage "{self.name}" {self.health}/{self.spawn_health}')

		if self.health == 0:
			self.state = self.DEAD

			if self.logger != None:
				self.logger.add(f'killing "{self.name}" {self.health}/{self.spawn_health}')

		# ressurect
		if self.state == self.DEAD:
			self.path = []
			self.target = geometry.position - glm.vec3(0.5, 0, 0.5)
			self.wait_time = self.ressurect_time
			self.health = self.spawn_health
			self.state = self.WAITING_DEAD

			if self.logger != None:
				self.logger.add(f'ressurecting "{self.name}" in {round(self.wait_time / 1000, 2)} seconds')

		if self.state == self.WAITING_DEAD and self.wait_time == 0:
			self.state = self.IDLE
			self.position = self.spawn_point
			self.target = self.spawn_point - glm.vec3(0.5, 0, 0.5)

		# generate random wait time when idle
		if self.state == self.IDLE:
			self.wait_time = random.uniform(self.wait_time_options[0], self.wait_time_options[1])
			self.state = self.WAITING

			if self.logger != None:
				self.logger.add(f'idling "{self.name}" for {round(self.wait_time / 1000, 2)} seconds')

		# generate walk path on wait time finish
		if self.state == self.WAITING and len(self.path) == 0 and self.wait_time == 0:
			# random angle and radius
			theta = random.uniform(0, 2 * math.pi)
			radius = random.uniform(0, self.radius)
			# radom point within radius
			x = self.spawn_point.x - 0.5 + radius * math.cos(theta)
			z = self.spawn_point.z - 0.5 + radius * math.sin(theta)

			start = (math.floor(geometry.position.x), math.floor(geometry.position.z))
			end = (math.floor(x), math.floor(z))

			self.path = astar(self.obstacles, start, end)
			self.state = self.WALKING

			if self.logger != None:
				self.logger.add(f'moving "{self.name}" from {start} to {end}')

		# go back to idle when finished walking
		if self.state == self.WALKING and len(self.path) == 0:
			self.state = self.IDLE
