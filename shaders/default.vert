#version 330

// frustum culling
#define OFFSET 0
#define IS_IN_VIEW(p) (abs(p.x) + OFFSET <= p.w && abs(p.y) + OFFSET <= p.w && p.z >= 0 && p.z + OFFSET <= p.w)
#define OFFSCREEN_POINT vec4(2, 2, 2, 1)
#define TRANSFORM(p) IS_IN_VIEW(vec4(p)) ? p : OFFSCREEN_POINT
// END frustum culling

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec2 texture_coords;
layout (location = 3) in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float transparency;
uniform float instance_index = 0;

out vec3 frag_normal;
out vec4 frag_color;
out float frag_transparency;
out vec3 frag_position;
out vec2 frag_texture_coords;

void main() {
	gl_Position = TRANSFORM(projection * view * model * vec4(in_position, 1.0));

	frag_normal = mat3(transpose(inverse(model))) * in_normal;
	frag_color = vec4(in_color, 1);
	frag_transparency = transparency;
	frag_position = vec3(model * vec4(in_position, 1.0));

	frag_texture_coords = texture_coords;
}
