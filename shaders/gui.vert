#version 330

layout (location = 0) in vec2 in_position;

uniform mat4 model;

void main() {
    gl_Position = model * vec4(in_position, 0.0, 1.0);
}
