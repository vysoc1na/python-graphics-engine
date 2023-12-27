from core.renderer import Renderer
from core.scene import Scene

renderer = Renderer()

scene = Scene(renderer)

renderer.run(scene)
