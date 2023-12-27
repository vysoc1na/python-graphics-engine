import pygame as pg
import glm
import math

from src.core.mesh import Mesh, MeshComponent

from src.components import Cursor, Player

from src.utils.astar import astar
from src.utils.queue import Action

class Chunk():
	def __init__(
		self,
		app,
		config,
		name = 'chunk',
		position = [0, 0, 0],
		size = 10,
	):
		self.app = app
		self.config = config
		self.name = name
		self.size = size

		self.components = {}
		self.children = {}

		self.set_position(position)
		self.is_mounted = False

	def mount(self):
		if self.is_mounted == True:
			return

		# make renderable vao's for individual mesh components
		components = self.config['components']
		for component in components:
			self.components[component['name']] = MeshComponent(
				app = self.app,
				shader_program = self.app.shader_program.programs[component['shader']],
				name = component['name'],
				parent = component.get('parent', None),
			)
		# compose all children for scene to render
		children = self.config['children']
		for item in children:
			# update position relative to chunk position
			position = glm.vec3(item.get('position', [0, 0, 0]))
			position.x += self.position.x * self.size + 0.5
			position.z += self.position.z * self.size + 0.5
			mesh_constructor = Mesh(
				app = self.app,
				mesh_component = self.components[item['type']],
				name = item['name'],
				position = position,
				scale = item.get('scale', [1, 1, 1]),
				color = item.get('color', None),
			)
			self.children[item['name']] = self.assign_mesh_parent(mesh_constructor)

		size = self.app.scene.config['size']
		#row_index = 0
		#for point in self.config['obstacles']:
		#	name = f'tile-{point[0]},{point[1]}'
		#	position = glm.vec3(item.get('position', [-size / 2, 1.1, size / 2]))
		#	position.x += self.position.x * self.size + 1 + point[0]
		#	position.z += self.position.z * self.size - point[1]
		#	self.children[name] = Mesh(
		#		app = self.app,
		#		mesh_component = self.components['tile'],
		#		name = name,
		#		position = position,
		#		transparency = 0.5,
		#		color = [1, 0, 0],
		#	)

		position = glm.vec3(33, 0.2, 32)
		self.children['pathfinder'] = Mesh(
			app = self.app,
			mesh_component = self.components['tile'],
			name = 'pathfinder',
			position = position,
			color = [0, 0, 0],
			scale = [0.5, 0.5, 0.5],
		)
		self.app.camera.target = position
		self.app.camera.new_target = position
		self.app.camera.rotate(75)

		self.is_mounted = True

		self.children['finish'] = Mesh(
			app = self.app,
			mesh_component = self.components['tile'],
			name = 'finish',
			position = (-31, 1, -30),
			scale = [0.8, 1, 0.8],
			color = [0, 1, 0],
			transparency = 0.5,
		)

	def render(self):
		if self.is_mounted == False:
			return

		for key in list(self.children):
			self.children[key].render()

	def destroy(self):
		if self.is_mounted == False:
			return

		for key in list(self.children):
			self.children[key].destroy()

		self.components.clear()
		self.children.clear()

		self.is_mounted = False

	def check_event(self, event):
		# call events only in rendered chunks
		if self.is_mounted == False:
			return

		if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]:
			position = self.children['pathfinder'].position
			target = self.app.scene.children['cursor'].data.position
			self.set_path(
				(position.x, position.z), (target.x, target.z)
			)

		for key in list(self.children):
			item = self.children[key]
			check_event_method = getattr(item, 'check_event', None)

			if callable(check_event_method):
				self.children[key].check_event(event)

	def set_position(self, position):
		self.position = glm.vec3(position)

	def assign_mesh_parent(self, mesh_constructor):
		if mesh_constructor.mesh.parent == 'model/cursor':
			return Cursor(self.app, mesh_constructor)

		if mesh_constructor.mesh.parent == 'model/player':
			return Player(self.app, mesh_constructor)

		return mesh_constructor

	def get_depth(self, x, y):
		depth_attachment = self.app.ctx.depth_texture((self.app.window_size[0], self.app.window_size[1]))
		fbo = self.app.ctx.framebuffer(depth_attachment = depth_attachment)
		fbo.clear()
		fbo.use()

		self.render()

		depth_data = fbo.read(components = 1, dtype = 'f4', attachment = -1)
		depth_array = np.frombuffer(depth_data, dtype=np.float32)

		normalized_depth = (depth_array - np.min(depth_array)) / (np.max(depth_array) - np.min(depth_array))
		clipped_depth = np.clip(normalized_depth, 0, 1)
		depth_data_flipped = np.flipud(clipped_depth.reshape((self.app.window_size[1], self.app.window_size[0])))

		return depth_data_flipped[y - 1, x - 1]

	def set_path(self, source = (0, 0), target = (31, 31)):
		self.app.queue.clear()

		for key in list(self.children):
			if self.children[key].name.startswith('tile-path-') == True:
				del self.children[key]

		if source == None:
			return

		size = self.app.scene.config['size']
		half_size = size / 2

		source = (round(source[0]), round(source[1]))
		target = (round(target[0]), round(target[1]))

		source = (int(source[0] + half_size - 1), int((source[1] - half_size) * -1))
		target = (int(target[0] + half_size - 1), int((target[1] - half_size) * -1))

		self.path = astar(self.config['obstacles'], source, target, 10)

		if self.path == None:
			return

		for item in self.path:
			name = f'tile-path-{item[0]},{item[1]}'
			position = glm.vec3(-size / 2, 0.2, size / 2)
			position.x += self.position.x * self.size + 1 + item[0]
			position.z += self.position.z * self.size - item[1]
			self.children[name] = Mesh(
				app = self.app,
				mesh_component = self.components['tile'],
				name = name,
				position = position,
				transparency = 0.1,
				color = [0, 0, 0],
				scale = [0.2, 0.2, 0.2],
			)

		self.path_index = 0
		def move(app):
			node = self.path[self.path_index]

			position = glm.vec3(-size / 2, 0.2, size / 2)
			position.x += self.position.x * self.size + 1 + node[0]
			position.z += self.position.z * self.size - node[1]

			original_position = self.children['pathfinder'].position
			self.children['pathfinder'].new_position = position

			direction = glm.normalize(original_position - position)
			rotation = self.direction_to_rotation(direction)

			camera_target = glm.vec3(
				position.x + direction.x,
				10,
				position.z + direction.z,
			)
			self.app.camera.move_to(self.app.camera.position - direction)
			self.app.camera.new_target = position

			self.path_index += 1

			if self.path_index == len(self.path):
				self.set_path(None)

		for node in self.path:
			self.app.queue.add(Action(move))

	def direction_to_rotation(self, direction_vector):
		direction_vector = direction_vector * glm.vec3(-1, 1, 1)
		direction = glm.normalize(glm.vec3(direction_vector))

		angle = math.atan2(direction.x, direction.z)
		angle_degrees = glm.degrees(angle)

		return angle_degrees + 270
