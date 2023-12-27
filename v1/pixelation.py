import moderngl
import pygame
import numpy as np

pygame.init()

# opengl attribute setup
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

# opengl context
width, height = 800, 600
pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

# Initialize ModernGL
ctx = moderngl.create_context()

# Create vertex shader
vertex_shader_source = """
#version 330
in vec2 in_position;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

# Create fragment shader
fragment_shader_source = """
#version 330
uniform float pixelation;
out vec4 fragColor;

void main() {
    ivec2 uv = ivec2(gl_FragCoord.xy / pixelation);
    vec2 newUV = vec2(uv) * pixelation / vec2(800, 600);  // Replace with actual resolution

    fragColor = vec4(newUV.x, newUV.y, 0.0, 1.0);  // Color based on coordinates
}
"""

# Create shader program
prog = ctx.program(vertex_shader=vertex_shader_source, fragment_shader=fragment_shader_source)

# Create vertex buffer
vertices = np.array([-1, -1, 1, -1, 1, 1, -1, 1], dtype='f4')
vbo = ctx.buffer(vertices)
vao = ctx.simple_vertex_array(prog, vbo, 'in_position')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render scene with pixelation
    ctx.clear()
    prog['pixelation'].value = 10.0  # Adjust this value for the level of pixelation
    vao.render(moderngl.TRIANGLE_FAN)

    pygame.display.flip()
    pygame.time.wait(10)  # Add a small delay to avoid high CPU usage

pygame.quit()
