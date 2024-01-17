import numpy
import glm
import moderngl

class Particles():
	def __init__(
		self,
		renderer,
		position = (0, 0, 0),
		count = 1000,
		decay_factor = 0.001,
		lifespan = (4, 8),
		radius = (1, 1, 1),
		speed = 0.02,
		color = (1, 1, 1),
		transparency = 1,
		point_size = 2,
	):
		self.renderer = renderer
		self.ctx = renderer.ctx
		self.shader_program = renderer.shaders['particles']

		self.position = position
		self.count = count
		self.decay_factor = decay_factor
		self.lifespan = lifespan
		self.radius = radius
		self.radius_half = (radius[0] / 2, radius[1] / 2, radius[2] / 2)
		self.speed = speed
		self.speed_half = speed / 2
		self.color = color
		self.transparency = transparency
		self.point_size = point_size

		self.on_init()

	def on_init(self):
		self.generate_particles_data()

		self.vbo_data = numpy.zeros(self.count, dtype=[('in_position', 'f4', 3), ('in_color', 'f4', 4)])
		self.vbo_data['in_position'] = self.particle_positions
		self.vbo_data['in_color'] = self.particle_colors

		self.vbo = self.ctx.buffer(self.vbo_data.tobytes())
		self.vao = self.ctx.simple_vertex_array(self.shader_program, self.vbo, 'in_position', 'in_color')

		self.model = glm.rotate(glm.mat4(1.0), 0, glm.vec3(0.0, 1.0, 0.0))

	def generate_particles_data(self, reset_indices = None):
		if reset_indices == None:
			self.particle_positions = numpy.random.rand(self.count, 3) * self.radius - self.radius_half
			self.particle_velocities = numpy.random.rand(self.count, 3) * self.speed - self.speed_half
			self.particle_lifespans = numpy.random.uniform(self.lifespan[0], self.lifespan[1], self.count)
			self.particle_colors = numpy.full([self.count, 4], (*self.color, self.transparency), dtype = 'float32')
		else:
			self.particle_positions[reset_indices] = numpy.random.rand(len(reset_indices[0]), 3) * self.radius - self.radius_half
			self.particle_velocities[reset_indices] = numpy.random.rand(len(reset_indices[0]), 3) * self.speed - self.speed_half
			self.particle_lifespans[reset_indices] = numpy.random.uniform(self.lifespan[0], self.lifespan[1], len(reset_indices[0]))

	def render(self, projection, view, ctx, render_mode):
		self.ctx.point_size = self.point_size

		self.particle_positions += self.particle_velocities
		self.particle_lifespans -= self.decay_factor * self.renderer.delta_time

		self.generate_particles_data(numpy.where(self.particle_lifespans < 0))

		self.shader_program['model'].write(self.model)
		self.shader_program['view'].write(view)
		self.shader_program['projection'].write(projection)

		self.vbo_data['in_position'] = self.particle_positions + self.position
		self.vbo.write(self.vbo_data.tobytes())

		self.vao.render(moderngl.POINTS)

	def destroy(self):
		self.vbo.release()
		self.vao.release()
