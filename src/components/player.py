import pygame as pg
import numpy as np
import glm
import math

class Player():
	def __init__(self, app, data):
		self.app = app
		self.data = data

		self.position = data.position
		self.rotation = data.rotation
		self.direction = glm.vec3(0, 0, 0)

	def render(self):
		self.update(self.app.time)

		self.data.render()

	def destroy(self):
		self.data.destroy()

	def update(self, time):
		# update camera position
		#self.app.camera.position = self.data.position + glm.vec3(0, 10, 0)
		#self.app.camera.yaw = -180
		#self.app.camera.pitch = -65

		# animate object position
		if self.direction.x != 0 or self.direction.z != 0:
			self.move_to_target()

		self.data.update()

	def check_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]:
			self.position = self.app.scene.children['cursor'].data.position

			# setup direction vector for position animation
			direction = self.position - self.data.position
			self.direction = glm.normalize(direction)

			# setup rotation to clicked point
			new_angle = self.direction_to_rotation(self.direction)
			self.data.rotation.y = new_angle

	def move_to_target(self):
		velocity = 0.005 * self.app.delta_time
		new_position = self.data.position + (self.direction * velocity)
		self.data.position = new_position

		distance = glm.length(self.position - self.data.position)

		if distance < 0.09:
			self.data.position = self.position
			self.direction = glm.vec3(0, 0, 0)

	def direction_to_rotation(self, direction_vector):
		direction = glm.normalize(glm.vec3(direction_vector))

		angle = math.atan2(direction.x, direction.z)
		angle_degrees = glm.degrees(angle)

		return angle_degrees + 90
