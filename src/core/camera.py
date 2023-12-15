import glm
import math
import pygame as pg
import moderngl as mgl
import numpy as np

class Camera():
	def __init__(self, app, position = (0, 0, 5), yaw = -90, pitch = 0):
		self.app = app

		# constants
		self.FOV = 45
		self.NEAR = 0.1
		self.FAR = 100
		self.ASPECT_RATIO = app.window_size[0] / app.window_size[1]
		self.SPEED = 0.005
		self.SENSITIVITY = 0.1

		# config
		self.position = glm.vec3(position)
		self.up = glm.vec3(0, 1, 0)
		self.right = glm.vec3(1, 0, 0)
		self.forward = glm.vec3(0, 0, -1)
		self.yaw = yaw
		self.pitch = pitch

		# projection
		self.m_view = self.get_view_matrix()
		self.m_proj = self.get_projection_matrix()

	def update(self):
		self.move()
		self.rotate()

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

		self.position.y = 0.8

		# keep light with camera
		self.app.light.position.x = self.position.x
		self.app.light.position.z = self.position.z

	def rotate(self):
		rel_x, rel_y = pg.mouse.get_rel()

		if pg.mouse.get_pressed()[0] == True:
			self.yaw += rel_x * self.SENSITIVITY
			self.pitch -= rel_y * self.SENSITIVITY
			self.pitch = max(-89, min(89, self.pitch))

	def get_view_matrix(self):
		return glm.lookAt(self.position, self.position + self.forward, self.up)

	def get_projection_matrix(self):
		return glm.perspective(self.FOV, self.ASPECT_RATIO, self.NEAR, self.FAR)
