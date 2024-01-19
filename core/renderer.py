import pygame
import moderngl
import sys

class Renderer():
	DEFAULT_CONFIG = {
		'width': 2560 / 3,
		'height': 1600 / 3,
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
		self.elapsed_time = 1
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
		# auto released unused objects
		self.ctx.gc_mode = 'auto'

	def setup_shaders(self):
		# default shader
		with open('shaders/default.vert', 'r') as vertex_shader_file:
			default_vertex_shader = vertex_shader_file.read()
		with open('shaders/default.frag', 'r') as fragment_shader_file:
			default_fragment_shader = fragment_shader_file.read()
		# gui shader
		with open('shaders/gui.vert', 'r') as vertex_shader_file:
			gui_vertex_shader = vertex_shader_file.read()
		with open('shaders/gui.frag', 'r') as fragment_shader_file:
			gui_fragment_shader = fragment_shader_file.read()
		# particles shader
		with open('shaders/particles.vert', 'r') as vertex_shader_file:
			particles_vertex_shader = vertex_shader_file.read()
		with open('shaders/particles.frag', 'r') as fragment_shader_file:
			particles_fragment_shader = fragment_shader_file.read()

		# grass shader
		with open('shaders/grass.vert', 'r') as vertex_shader_file:
			grass_vertex_shader = vertex_shader_file.read()
		# water shader
		with open('shaders/water.vert', 'r') as vertex_shader_file:
			water_vertex_shader = vertex_shader_file.read()

		# shaders dict
		self.shaders = {
			'default': self.ctx.program(
				vertex_shader = default_vertex_shader,
				fragment_shader = default_fragment_shader,
			),
			'gui': self.ctx.program(
				vertex_shader = gui_vertex_shader,
				fragment_shader = gui_fragment_shader,
			),
			'particles': self.ctx.program(
				vertex_shader = particles_vertex_shader,
				fragment_shader = particles_fragment_shader,
			),
			'grass': self.ctx.program(
				vertex_shader = grass_vertex_shader,
				fragment_shader = default_fragment_shader,
			),
			'water': self.ctx.program(
				vertex_shader = water_vertex_shader,
				fragment_shader = default_fragment_shader,
			),
		}

	def check_events(self, gui, scene, camera):
		for event in pygame.event.get():
			# global program close event
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				# end run loop and destroy scene
				self.is_running = False
				scene.destroy()
				gui.destroy()
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
			# camera zoom handler
			if event.type == pygame.MOUSEWHEEL:
				# camera controls
				camera.set_zoom(event)
			# gui mouse up event
			if event.type == pygame.MOUSEBUTTONUP:
				for item in gui.children:
					item.handle_on_click()

	def render(self, gui, scene, camera):
		# show fps in window caption
		pygame.display.set_caption(f'{round(self.clock.get_fps(), 2)}')
		# clear original frame buffer
		self.ctx.screen.use()
		self.ctx.clear(color = (1, 1, 1, 0), depth = True)
		# render scene
		scene.render(camera)
		# render gui
		gui.render()
		# swap buffers
		pygame.display.flip()

	def run(self, gui, scene, camera):
		self.is_running = True
		# start the render loop
		while self.is_running == True:
			# render scene and gui
			self.render(gui, scene, camera)
			# check for event listeners
			self.check_events(gui, scene, camera)
			# camera movement
			camera.controls(self.delta_time)
			# get next screen
			self.delta_time = self.clock.tick(60)
			self.elapsed_time = pygame.time.get_ticks()
