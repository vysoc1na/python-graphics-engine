import pygame as pg
import numpy as np
import math
import glm
import json

from src.core.chunk import Chunk
from src.core.mesh import Mesh, MeshComponent

from src.components.cursor import Cursor

class Scene():
	def __init__(self, app, config):
		self.app = app
		self.ctx = app.ctx
		self.config = config

		self.components = {}
		self.children = {}

		self.chunks = {}

		self.on_init()

	def on_init(self):
		# Get all chunk instances and assign them to Scene
		for chunk in self.config['chunks']:
			self.chunks[chunk['name']] = self.get_chunk_isntance(chunk)

		# Custom cursor pointer component
		self.components['cursor'] = MeshComponent(
			app = self.app,
			shader_program = self.app.shader_program.programs['default'],
			name = 'cursor',
			parent = 'model/cursor'
		)
		self.children['cursor'] = Cursor(
			app = self.app,
			data = Mesh(
				app = self.app,
				mesh_component = self.components['cursor'],
				name = 'cursor',
			)
		)

	def render(self, t):
		camera_position =  self.app.camera.position

		# Render children that are direct descendants of Scene
		for _, key in enumerate(self.children):
			self.children[key].render()

		# Render chunks that are in a range of camera
		for key in self.chunks:
			chunk = self.chunks[key]
			chunk_x = chunk.position.x * self.config['size']
			chunk_z = chunk.position.z * self.config['size']

			if self.is_chunk_in_radius(chunk_x, chunk_z, camera_position.x, camera_position.z):
				chunk.mount()
				chunk.render()
			else:
				chunk.destroy()

	def destroy(self):
		# Destroy children that are direct descendants of Scene
		for _, key in enumerate(self.children):
			self.children[key].destroy()

		# Destroy all chunk instances
		for _, key in enumerate(self.chunks):
			self.chunks[key].destroy()

		self.components.clear()
		self.children.clear()

	def check_event(self, event):
		for _, key in enumerate(self.children):
			item = self.children[key]
			check_event_method = getattr(item, 'check_event', None)

			if callable(check_event_method):
				self.children[key].check_event(event)

		for _, key in enumerate(self.chunks):
			self.chunks[key].check_event(event)

	def is_chunk_in_radius(self, chunk_x, chunk_y, camera_x, camera_y):
		# Calculate the squared distance between the chunk center and the camera
		squared_distance = (chunk_x - camera_x) ** 2 + (chunk_y - camera_y) ** 2

		# Check if the squared distance is within the squared radius
		return squared_distance <= (self.config['size'] * 2) ** 2

	def get_chunk_isntance(self, chunk):
		name = chunk['name']
		position = chunk['position']
		with open(f'config/{name}.json', 'r') as chunk_config:
			return Chunk(
				app = self.app,
				config = json.load(chunk_config),
				name = name,
				position = position,
				size = self.config['size'],
			 )

	def screen_to_world(self, x, y, depth = 0, wy = 0):
		# Normalize screen coordinates to the range [-1, 1]
		xx = (2 * x) / self.app.window_size[0] - 1
		yy = (2 * (self.app.window_size[1] - y)) / self.app.window_size[1] - 1
		# Define near and far depth values in normalized device coordinates
		zzN = 0
		zzF = 1

		# Calculate the inverse of the combined projection and view matrix
		invM = glm.inverse(self.app.camera.m_proj * self.app.camera.m_view)

		# Transform screen coordinates to world coordinates for near and far depths
		mmN = invM * glm.vec4(xx, yy, zzN, 1)
		mmF = invM * glm.vec4(xx, yy, zzF, 1)

		# Normalize the coordinates by dividing by the w component
		nn = glm.vec3(mmN[0] / mmN[3], mmN[1] / mmN[3], mmN[2] / mmN[3])
		ff = glm.vec3(mmF[0] / mmF[3], mmF[1] / mmF[3], mmF[2] / mmF[3])

		# Interpolate between near and far coordinates based on depth
		t = nn[1] / (nn[1] - ff[1])
		wx = nn[0] + (ff[0] - nn[0]) * t
		wz = nn[2] + (ff[2] - nn[2]) * t

    	# Return the final world coordinates
		return glm.vec3(wx, wy, wz)
