import pygame as pg
import moderngl as mgl
import sys
import json

from src.core.camera import Camera
from src.core.light import Light
from src.core.shader import ShaderProgram
from src.core.scene import Scene

class Renderer():
	def __init__(self, config):
		self.config = config
		# init pygame modules
		pg.init()
		# global window size
		self.window_size = (self.config['width'], self.config['height'])
		# opengl attribute setup
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
		# opengl context
		pg.display.set_mode(self.window_size, flags = pg.OPENGL | pg.DOUBLEBUF) # | pg.FULLSCREEN
		self.ctx = mgl.create_context()
		self.ctx.enable(mgl.DEPTH_TEST | mgl.BLEND)
		# global clock
		self.clock = pg.time.Clock()
		self.time = 0
		self.delta_time = 0
		# shader program
		self.shaderProgram = ShaderProgram(self.ctx)
		# scene
		self.light = Light(position = (0, 10, 0), color = (1, 1, 1))
		self.camera = Camera(self, position = (3, 5, 3), yaw = -135, pitch = -45)
		self.scene = Scene(self)

	def check_events(self):
		for event in pg.event.get():
			self.scene.check_event(event)
			# event for program close
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				self.scene.destroy()
				pg.quit()
				sys.exit()

	def render(self):
		# clear frame buffer
		self.ctx.screen.use()
		self.ctx.clear(color = (0, 0, 0))
		# render scene
		self.scene.render(self.time)
		# swap buffers
		pg.display.flip()
		# show fps in caption
		caption = self.config['caption']
		# caption - ray position
		rayX, rayZ = round(self.scene.cursor.x, 2), round(self.scene.cursor.z, 2)
		caption = caption.replace('[rayX]', f'{rayX}').replace('[rayZ]', f'{rayZ}')
		# captin - fps
		caption = caption.replace('[fps]', f'{round(self.clock.get_fps(), 2)}')
		pg.display.set_caption(caption)

	def run(self):
		while True:
			self.time = pg.time.get_ticks()

			self.check_events()
			self.camera.update()
			self.render()

			self.delta_time = self.clock.tick(60)

with open('config/window.json', 'r') as f:
	app = Renderer(config = json.load(f))
	app.run()



