import pygame
import moderngl
import sys

class Renderer():
	DEFAULT_CONFIG = {
		'width': 800,
		'height': 600,
	}

	def __init__(self, config = None):
		# setup config
		self.setup_config(config)
		# setup pygame / moderngl
		self.setup_pygame()
		self.setup_moderngl()
		# setup shaders
		self.setup_shaders()

	def setup_config(self, config):
		# general config
		self.config = config or self.DEFAULT_CONFIG
		self.window_size = (self.config['width'], self.config['height'])
		# pygme / moderngl config
		self.render_mode = moderngl.TRIANGLES

	def setup_pygame(self):
		# pygames core init
		pygame.init()
		# gloval game clock
		self.clock = pygame.time.Clock()
		self.delta_time = 1
		self.is_running = False

	def setup_moderngl(self):
		# opengl attribute setup
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
		pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
		# opengl context
		pygame.display.set_mode(self.window_size, flags = pygame.OPENGL | pygame.DOUBLEBUF)
		self.ctx = moderngl.create_context()
		self.ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)
		self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
		self.ctx.blend_equation = moderngl.FUNC_ADD

	def setup_shaders(self):
		# default shader
		with open('shaders/default.vert', 'r') as vertex_shader_file:
			default_vertex_shader = vertex_shader_file.read()
		with open('shaders/default.frag', 'r') as fragment_shader_file:
			default_fragment_shader = fragment_shader_file.read()
		# shaders dict
		self.shaders = {
			'default': self.ctx.program(
				vertex_shader = default_vertex_shader,
				fragment_shader = default_fragment_shader,
			),
		}

	def check_events(self, scene, camera):
		for event in pygame.event.get():
			# global program close event
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				# end run loop and destroy scene
				self.is_running = False
				scene.destroy()
				# quit program
				pygame.quit()
				sys.exit()
			# switch between render modes
			if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
				self.render_mode = moderngl.TRIANGLES
			if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
				self.render_mode = moderngl.LINES
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				self.render_mode = moderngl.POINTS
			# component events
			# TODO scene.check_event(event)

	def render(self, scene, camera):
		# show fps in window caption
		pygame.display.set_caption(f'{round(self.clock.get_fps(), 2)}')
		# clear original frame buffer
		self.ctx.screen.use()
		self.ctx.clear(color = (1, 1, 1, 0))
		# render scene
		scene.render(camera)
		# swap buffers
		pygame.display.flip()

	def run(self, scene, camera):
		self.is_running = True
		# start the render loop
		while self.is_running == True:
			# check for event listeners
			self.check_events(scene, camera)
			# camera movement
			camera.controls(self.delta_time)
			# render scene
			self.render(scene, camera)
			# get next screen
			self.delta_time = self.clock.tick(60)
