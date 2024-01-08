import math

from core.renderer import Renderer
from core.gui import Gui, GuiElement
from core.scene import Scene
from core.camera import Camera

from components.terrain import Terrain
from components.obstacles import Obstacles
from components.entity_player import Player
from components.entity_enemy import Enemy
from components.cursor import Cursor

renderer = Renderer()

gui = Gui(renderer)
scene = Scene(renderer)
camera = Camera(renderer)

# generate obstacles data
obstacles_data = []
for x in range(16):
	for z in range(16):
		if (x == 1 or x == 15) and z > 0:
			obstacles_data.append({ 'position': [x, 0, z] })
		if (z == 1 or z == 15) and x > 1 and x < 15:
			obstacles_data.append({ 'position': [x, 0, z] })

factor = 20
for theta in range(factor):
	x = 8.5 + 4 * math.cos(math.radians(theta * (360 / factor)))
	z = 8.5 + 4 * math.sin(math.radians(theta * (360 / factor)))
	floor_x, floor_z = math.floor(x), math.floor(z)
	if floor_x != 4 and floor_z != 4:
		obstacles_data.append({ 'position': [floor_x, 0, floor_z] })

# Terrain
terrain = Terrain(renderer)
# Terrain Obstacles
obstacles = Obstacles(
	renderer,
	terrain_component = terrain,
	obstacles_data = obstacles_data,
)
# Player Entity
player = Player(
	renderer,
	position = (1, 0, 1),
	terrain_component = terrain,
	obstacles_component = obstacles,
	camera_component = camera,
)
# Enemy Entity
enemy = Enemy(
	renderer,
	position = (8, 0, 8),
	terrain_component = terrain,
	obstacles_component = obstacles,
)
# Cursor Entity
cursor = Cursor(
	renderer,
	position = (0, 0, 0),
	terrain_component = terrain,
	obstacles_component = obstacles,
	camera_component = camera,
)

# compose scene
scene.children.append(player.mesh)
scene.children.append(enemy.mesh)
scene.children.append(terrain.mesh)
scene.children.append(cursor.mesh)
scene.children.append(obstacles.mesh)

# GUI Element
button = GuiElement(renderer)

# compose gui
gui.children.append(button)

renderer.run(gui, scene, camera)
