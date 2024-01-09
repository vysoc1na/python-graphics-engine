#version 330

layout (location = 0) in vec2 in_position;
layout (location = 1) in vec2 in_texture_coords;

out vec2 frag_text_coord;

uniform mat4 model;

void main() {
    gl_Position = model * vec4(in_position, 0.0, 1.0);
    frag_text_coord = in_texture_coords;
}
