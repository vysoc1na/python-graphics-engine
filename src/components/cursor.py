import pygame as pg
import glm

class Cursor():
	def __init__(self, app, data, size = 1, height = 0):
		self.app = app
		self.data = data

		self.size = size
		self.height = height

		# setup scale
		self.scale = glm.vec3(self.size / 2, self.size / 2, self.size / 2)
		self.data.set_scale(self.scale)

	def render(self):
		self.update(self.app.time)

		self.data.render()

	def destroy(self):
		self.data.destroy()

	def update(self, time):
		# get and convert screen to world coordinates
		x, y = pg.mouse.get_pos()
		world_coords = self.app.scene.screen_to_world(x, y, 0, self.height)
		# round and scale cursor
		position = glm.vec3(
			self.round_to_grid(world_coords.x, self.size),
			world_coords.y,
			self.round_to_grid(world_coords.z, self.size),
		)
		# set new properties
		self.data.set_position(position)

		# transparency
		self.data.set_transparency(0.9)

		self.data.update()

	def round_to_grid(self, x, base = 5):
		return base * round(x / base)

	def check_event(self, event):
		scale_factor = glm.vec3(0.1, 0, 0.1)

		if event.type == pg.MOUSEBUTTONDOWN:
			self.data.set_scale(self.scale - scale_factor)
		if event.type == pg.MOUSEBUTTONUP:
			self.data.set_scale(self.scale)
