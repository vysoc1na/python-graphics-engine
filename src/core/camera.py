import glm
import math
import pygame as pg
import moderngl as mgl
import numpy as np

from src.utils.transition import transition_vec3, transition_float

class Camera():
	def __init__(self, app, position = (0, 0, 5), yaw = -90, pitch = 0):
		self.app = app

		# constants
		self.FOV = 45
		self.NEAR = 0.1
		self.FAR = 100
		self.ASPECT_RATIO = app.window_size[0] / app.window_size[1]
		self.SPEED = 0.01
		self.SENSITIVITY = 0.1

		# config
		self.position = glm.vec3(position)
		self.up = glm.vec3(0, 1, 0)
		self.right = glm.vec3(1, 0, 0)
		self.forward = glm.vec3(0, 0, -1)
		self.yaw = yaw
		self.pitch = pitch
		# rotate aorund target
		self.target = None
		self.radius = 14
		self.theta = -yaw
		self.phi = -pitch
		# transitions
		self.new_position = glm.vec3(position)
		self.new_target = None
		self.rel_x = 0
		self.new_rel_x = 0
		self.rel_y = 0
		self.new_rel_y = 0

		# projection
		self.m_view = self.get_view_matrix()
		self.m_proj = self.get_projection_matrix()

	def update(self):
		self.move()
		self.rotate()

		delta_time = self.app.delta_time

		# animate values between each other
		self.target = transition_vec3(self.target, self.new_target, delta_time, 250)
		self.position = transition_vec3(self.position, self.new_position, delta_time, 250)
		# look at target at the end of animations

		self.rel_x = transition_float(self.rel_x, self.new_rel_x, delta_time, 100)
		self.rel_y = transition_float(self.rel_y, self.new_rel_y, delta_time, 100)
		self.new_rel_x = transition_float(self.new_rel_x, 0, delta_time, 100)
		self.new_rel_y = transition_float(self.new_rel_y, 0, delta_time, 100)

		if self.target != None:
			self.look_at(self.target)

		self.update_vectors()
		self.m_view = self.get_view_matrix()
		self.m_proj = self.get_projection_matrix()

	def update_vectors(self):
		yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

		self.forward.x = glm.cos(yaw) * glm.cos(pitch)
		self.forward.y = glm.sin(pitch)
		self.forward.z = glm.sin(yaw) * glm.cos(pitch)

		self.forward = glm.normalize(self.forward)
		self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
		self.up = glm.normalize(glm.cross(self.right, self.forward))

	def move(self):
		keys = pg.key.get_pressed()
		velocity = self.SPEED * self.app.delta_time

		if self.target == None:
			# speed up movement 3 times with LEFT CTRL
			if keys[pg.K_LCTRL]:
				velocity *= 3
			# movement of camera W A S D
			if keys[pg.K_w]:
				self.position += self.forward * velocity
			if keys[pg.K_a]:
				self.position -= self.right * velocity
			if keys[pg.K_s]:
				self.position -= self.forward * velocity
			if keys[pg.K_d]:
				self.position += self.right * velocity
			# elevation of camera SHIFT SPACE
			if keys[pg.K_LSHIFT]:
				self.position -= self.up * velocity
			if keys[pg.K_SPACE]:
				self.position += self.up * velocity
		else:
			if keys[pg.K_a]:
				self.rotate(x = self.SENSITIVITY * 50)
			if keys[pg.K_d]:
				self.rotate(x = -self.SENSITIVITY * 50)
			if keys[pg.K_w]:
				self.rotate(y = -self.SENSITIVITY * 50)
			if keys[pg.K_s]:
				self.rotate(y = self.SENSITIVITY * 50)

		# keep light with camera
		self.app.light.position.x = self.position.x
		self.app.light.position.z = self.position.z

	def rotate(self, x = 0, y = 0):
		rel_x, rel_y = pg.mouse.get_rel()

		if pg.mouse.get_pressed()[0] or (abs(x) > 0 or abs(y) > 0):
			self.new_rel_x = rel_x
			self.new_rel_y = rel_y

			if abs(x) > 0:
				self.new_rel_x = x
			if abs(y) > 0:
				self.new_rel_y = y

		if abs(self.rel_x) > 0 or abs(self.rel_y) > 0:
			self.theta += self.rel_x * self.SENSITIVITY
			self.phi -= self.rel_y * self.SENSITIVITY
			self.phi = max(-89, min(89, self.phi))

			if self.target is not None:
				theta = math.radians(self.theta)
				phi = math.radians(self.phi)

				self.new_position.x = self.target.x + self.radius * glm.cos(phi) * glm.cos(theta)
				self.new_position.y = self.target.y + self.radius * glm.sin(phi)
				self.new_position.z = self.target.z + self.radius * glm.cos(phi) * glm.sin(theta)
			else:
				self.yaw += self.rel_x * self.SENSITIVITY
				self.pitch -= self.rel_y * self.SENSITIVITY
				self.pitch = max(-89, min(89, self.pitch))

	def get_view_matrix(self):
		return glm.lookAt(self.position, self.position + self.forward, self.up)

	def get_projection_matrix(self):
		return glm.perspective(self.FOV, self.ASPECT_RATIO, self.NEAR, self.FAR)

	def look_at(self, target):
		target = glm.vec3(target)
		forward = glm.normalize(target - self.position) + glm.vec3(0.01, 0.01, 0.01) * glm.vec3(3, 3, 3)
		self.yaw = math.degrees(np.arctan2(forward.z, forward.x))
		self.pitch = math.degrees(np.arcsin(forward.y))

		if self.target == None:
			self.theta = -self.yaw
			self.phi = -self.pitch

	def move_to(self, target):
		self.new_position = target
