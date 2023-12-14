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
		# mount chunks
		for chunk in self.config['chunks']:
			self.chunks[chunk['name']] = self.get_chunk_isntance(chunk)

		self.chunks['chunk-0-0'].mount()
		#self.chunks['chunk-0-1'].mount()

		self.components['cursor'] = MeshComponent(
			app = self.app,
			shader_program = self.app.shader_program.programs['default'],
			name = 'cursor',
			parent = 'cursor'
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

		for _, key in enumerate(self.children):
			self.children[key].render()

		for _, key in enumerate(self.chunks):
			chunk = self.chunks[key]
			if self.is_chunk_in_radius(
				chunk.position.x * self.config['size'],
				chunk.position.z * self.config['size'],
				camera_position.x,
				camera_position.z,
			):
				chunk.mount()
			else:
				chunk.destroy()
			chunk.render()

	def is_chunk_in_radius(self, tile_x, tile_y, point_x, point_y):
		# Calculate the squared distance between the tile center and the point
		squared_distance = (tile_x - point_x)**2 + (tile_y - point_y)**2

		# Check if the squared distance is within the squared radius
		return squared_distance <= (self.config['size'] * 1.5)**2

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

	def destroy(self):
		for _, key in enumerate(self.children):
			self.children[key].destroy()

		for _, key in enumerate(self.chunks):
			self.chunks[key].destroy()

	def screen_to_world(self, x, y, depth = 0, wy = 0):
		xx = (2 * x) / self.app.window_size[0] - 1
		yy = (2 * (self.app.window_size[1] - y)) / self.app.window_size[1] - 1
		zzN = 0
		zzF = 1

		invM = glm.inverse(self.app.camera.m_proj * self.app.camera.m_view)

		mmN = invM * glm.vec4(xx, yy, zzN, 1)
		mmF = invM * glm.vec4(xx, yy, zzF, 1)

		nn = glm.vec3(mmN[0] / mmN[3], mmN[1] / mmN[3], mmN[2] / mmN[3])
		ff = glm.vec3(mmF[0] / mmF[3], mmF[1] / mmF[3], mmF[2] / mmF[3])

		t = nn[1] / (nn[1] - ff[1])
		wx = nn[0] + (ff[0] - nn[0]) * t
		wz = nn[2] + (ff[2] - nn[2]) * t

		return glm.vec3(wx, wy, wz)
