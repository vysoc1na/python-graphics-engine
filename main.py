import pygame as pg
import moderngl as mgl
import sys
import json

from src.core.camera import Camera
from src.core.light import Light
from src.core.shader import ShaderProgram
from src.core.scene import Scene

class Renderer():
	def __init__(self, config, scene_config):
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
		self.shader_program = ShaderProgram(self.ctx)
		# scene
		self.light = Light(position = (0, 10, 0), color = (1, 1, 1))
		self.camera = Camera(self, position = (3, 5, 3), yaw = -135, pitch = -15)
		self.scene = Scene(self, scene_config)

	def check_events(self):
		for event in pg.event.get():
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

		caption = self.config['caption']
		# caption - cursor position
		cursor = self.scene.children['cursor'].data.position
		caption = caption.replace('[cursorX]', f'{round(cursor.x, 1)}')
		caption = caption.replace('[cursorZ]', f'{round(cursor.z, 1)}')
		# caption - fps
		caption = caption.replace('[fps]', f'{round(self.clock.get_fps(), 2)}')
		# render caption
		pg.display.set_caption(caption)

	def run(self):
		while True:
			self.time = pg.time.get_ticks()

			self.check_events()
			self.camera.update()
			self.render()

			self.delta_time = self.clock.tick(60)

with open('config/window.json', 'r') as window_config:
	with open('config/scene.json', 'r') as scene_config:
		app = Renderer(
			config = json.load(window_config),
			scene_config = json.load(scene_config),
		)
		app.run()



