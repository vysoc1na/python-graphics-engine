import glm
import pygame

from utils.lerp import lerp

class Camera():
	def __init__(self, renderer, position = (0, 5, 0)):
		# setup context
		self.renderer = renderer
		self.ctx = renderer.ctx
		# constants
		self.speed = 0.01
		self.sensitivity = 0.01
		# movement / rotation
		self.front = glm.vec3(0, 0, -1)
		self.up = glm.vec3(0, 1, 0)
		self.right = glm.vec3(1, 0, 0)
		self.yaw = -90
		self.pitch = -45
		self.zoom = 0
		# setup mvp
		self.position = glm.vec3(position)
		self.setup_mvp()

	def setup_mvp(self):
		# constants
		fov = glm.radians(45.0)
		aspect_ratio = self.renderer.config['width'] / self.renderer.config['height']
		near_plane = 1
		far_plane = 64
		# mvp
		self.m_projection = glm.perspective(fov, aspect_ratio, near_plane, far_plane)
		self.m_view = glm.lookAt(self.position, self.position + self.front, self.up)
		self.m_model = glm.mat4(1.0)

	def controls(self, delta_time):
		# handle movement
		self.move(delta_time)
		# handle rotation
		self.rotate(delta_time)
		# decrease zoom
		self.zoom = lerp(self.zoom, 0, 0.1)

	def move(self, dt):
		keys = pygame.key.get_pressed()
		# get velocity
		velocity = self.speed * dt
		# camera movement
		if keys[pygame.K_w]:
			# self.position += velocity * self.front
			self.position -= velocity * self.up
		if keys[pygame.K_s]:
			# self.position -= velocity * self.front
			self.position += velocity * self.up
		if keys[pygame.K_a]:
			# self.position -= glm.normalize(glm.cross(self.front, self.up)) * velocity
			self.yaw += velocity * 10
		if keys[pygame.K_d]:
			# self.position += glm.normalize(glm.cross(self.front, self.up)) * velocity
			self.yaw -= velocity * 10

		if self.zoom != 0:
			self.position += (self.zoom * velocity) * self.up

		self.position.y = min(10, max(2.5, self.position.y))

	def rotate(self, dt):
		rel_x, rel_y = pygame.mouse.get_rel()
		# get velocity
		velocity = self.sensitivity * dt
		# camera rotation
		if pygame.mouse.get_pressed()[0]:
			self.yaw += rel_x * velocity
			#self.pitch -= rel_y * velocity
			#self.pitch = max(0, min(75, self.pitch))
		# update vectors
		yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
		self.front.x = glm.cos(yaw) * glm.cos(pitch)
		self.front.y = glm.sin(pitch)
		self.front.z = glm.sin(yaw) * glm.cos(pitch)
		self.front = glm.normalize(self.front)
		self.right = glm.normalize(glm.cross(self.front, glm.vec3(0, 1, 0)))
		self.up = glm.normalize(glm.cross(self.right, self.front))

	def set_zoom(self, event):
		if event.type == pygame.MOUSEWHEEL:
			self.zoom = event.y * -1
