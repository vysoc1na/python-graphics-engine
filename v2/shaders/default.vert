#version 330

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 frag_normal;
out vec4 frag_color;
out vec3 frag_position;

void main() {
    gl_Position = projection * view * model * vec4(in_position, 1.0);

    frag_normal = mat3(transpose(inverse(model))) * in_normal;
    frag_color = vec4(in_color, 1);
    frag_position = vec3(model * vec4(in_position, 1.0));
}
