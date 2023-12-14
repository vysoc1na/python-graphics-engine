import pygame as pg
import numpy as np
import math
import glm

from src.core.mesh import Mesh, MeshComponent

from src.components.cursor import Cursor

class Scene():
	def __init__(self, app, config):
		self.app = app
		self.ctx = app.ctx
		self.config = config

		self.components = {}
		self.children = {}

		self.cursor = glm.vec3(0, 0, 0)

		self.on_init()

	def on_init(self):
		"""
		# debug tiles
		self.components['tile'] = MeshComponent(
			app = self.app,
			shader_program = self.app.shaderProgram.programs['default'],
			name = 'tile'
		)
		n, s = 10, 2
		for x in range(-n, n, s):
			for z in range(-n, n, s):
				self.children[f'tile|{x},{z}'] = Mesh(
					app = self.app,
					mesh_component = self.components['tile'],
					position = (x, 0, z)
				)
		"""

		# make renderable vao's for individual mesh components
		components = self.config['components']
		for component in components:
			self.components[component['name']] = MeshComponent(
				app = self.app,
				shader_program = self.app.shaderProgram.programs[component['shader']],
				name = component['name'],
				parent = self.get_or(component, 'parent', None)
			)
		children = self.config['children']
		for item in children:
			mesh_constructor = Mesh(
				app = self.app,
				mesh_component = self.components[item['type']],
				name = item['name'],
				position = self.get_or(item, 'position', [0, 0, 0]),
				scale = self.get_or(item, 'scale', [1, 1, 1]),
			)
			self.children[item['name']] = self.assign_mesh_parent(mesh_constructor)

	@staticmethod
	def get_or(item, key, default):
		if key in item:
			return item[key]
		else:
			return default

	def assign_mesh_parent(self, mesh_constructor):
		if mesh_constructor.mesh.parent == 'cursor':
			return Cursor(self.app, mesh_constructor)

		return mesh_constructor

	# TODO: replace byc hunk implementation
	def is_renderable(self, item):
		return True

	def render(self, t):
		for _, key in enumerate(self.children):
			item = self.children[key]
			if self.is_renderable(item):
				item.render()

	def destroy(self):
		for _, key in enumerate(self.children):
			self.children[key].destroy()

	def get_depth(self, x, y):
		depth_attachment = self.app.ctx.depth_texture((self.app.window_size[0], self.app.window_size[1]))
		fbo = self.app.ctx.framebuffer(depth_attachment = depth_attachment)
		fbo.clear()
		fbo.use()

		for _, key in enumerate(self.children):
			item = self.children[key]
			if self.is_renderable(item):
				item.render()

		depth_data = fbo.read(components = 1, dtype = 'f4', attachment = -1)
		depth_array = np.frombuffer(depth_data, dtype=np.float32)

		normalized_depth = (depth_array - np.min(depth_array)) / (np.max(depth_array) - np.min(depth_array))
		clipped_depth = np.clip(normalized_depth, 0, 1)
		depth_data_flipped = np.flipud(clipped_depth.reshape((self.app.window_size[1], self.app.window_size[0])))

		return depth_data_flipped[y - 1, x - 1]

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
