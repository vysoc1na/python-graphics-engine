#version 330

// frustum culling
#define OFFSET 0
#define IS_IN_VIEW(p) (abs(p.x) + OFFSET <= p.w && abs(p.y) + OFFSET <= p.w && p.z >= 0 && p.z + OFFSET <= p.w)
#define OFFSCREEN_POINT vec4(2, 2, 2, 1)
#define TRANSFORM(p) IS_IN_VIEW(vec4(p)) ? p : OFFSCREEN_POINT
// END frustum culling

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 in_position;
in vec4 in_color;

out vec4 color;

void main() {
    gl_Position = TRANSFORM(projection * view * model * vec4(in_position, 1.0));
    color = in_color;
}
