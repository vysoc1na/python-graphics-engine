import pygame
import sys
import math
import glm

from utils.terrain_data import get_terrain_data
from utils.interpolate import interpolate

from core.renderer import Renderer
from core.font import Font
from core.gui import Gui
from core.scene import Scene
from core.camera import Camera
from core.particles import Particles

from gui.button import Button
from gui.button_list import ButtonList
from gui.console import Console

from components.terrain import Terrain
from components.obstacles import Obstacles
from components.entity_player import Player
from components.entity_enemy import Enemy
from components.cursor import Cursor
from components.grass import Grass

renderer = Renderer()

font = Font()
gui = Gui(renderer)
console = Console(renderer, font)

scene = Scene(renderer)
camera = Camera(renderer)

# Terrain
terrain = Terrain(renderer)
# generate obstacles data
obstacles_data = []
for item in get_terrain_data(terrain.geometry.height_map):
	corners = item['corners']
	top_interpolated = interpolate(corners[0], corners[1], 0.5)
	bottom_interpolated = interpolate(corners[2], corners[3], 0.5)
	interpolated_height = interpolate(top_interpolated, bottom_interpolated, 0.5)
	if interpolated_height < -0.15:
		position = item['position']
		obstacles_data.append({ 'position': [position.y + 1, -0.8, position.x + 1] })
# Terrain Obstacles
obstacles = Obstacles(
	renderer,
	terrain_component = terrain,
	obstacles_data = obstacles_data,
)
# Player Entity
player = Player(
	renderer,
	position = (32, 0, 32),
	terrain_component = terrain,
	obstacles_component = obstacles,
	camera_component = camera,
	logger = console,
)
# Enemy Entity
enemy = Enemy(
	renderer,
	position = (32, 0, 32),
	terrain_component = terrain,
	obstacles_component = obstacles,
	logger = console,
)
# Cursor Entity
cursor = Cursor(
	renderer,
	position = (0, 0, 0),
	terrain_component = terrain,
	obstacles_component = obstacles,
	camera_component = camera,
)
# Grass
grass = Grass(
	renderer,
	position = (32, 1, 32),
	terrain_component = terrain,
	obstacles_component = obstacles,
)
# Particles
particles = Particles(
	renderer,
	position = (32, -1, 32),
	radius = (32, 1, 32),
    color = (0, 1, 0.5),
    transparency = 0.5,
)

# compose scene
scene.children.append(player.mesh)
scene.children.append(enemy.mesh)
scene.children.append(terrain.mesh)
scene.children.append(grass.mesh)
scene.children.append(cursor.mesh)
scene.children.append(obstacles.mesh)
# compose particles scene
scene.children.append(particles)

# Button List
def respawn():
	console.add('respawn "player" at x: 32, z: 32')
	player.path = []
	player.target = glm.vec3(32, 0, 32)

def close_window():
	pygame.quit()
	sys.exit()

button_respawn = Button(renderer, font, text = 'respawn', on_click = respawn, corner = 'TL')
button_quit = Button(renderer, font, text = 'quit', on_click = close_window, corner = 'TL')

button_list = ButtonList(renderer, elements = [button_respawn, button_quit])

# compose gui
gui.children.append(button_list)
gui.children.append(console)

renderer.run(gui, scene, camera)
