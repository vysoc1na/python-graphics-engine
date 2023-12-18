import pygame as pg
import glm

class Cursor():
	def __init__(self, app, data, size = 1, height = 0):
		self.app = app
		self.data = data

		self.size = size
		self.height = height

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
		scale = [self.size / 2, self.size / 2, self.size / 2]
		# set new properties
		self.data.set_position(position)
		self.data.set_scale(scale)

		# transparency
		self.data.set_transparency(0.9)

		self.data.update()

	def round_to_grid(self, x, base = 5):
		return base * round(x / base)
