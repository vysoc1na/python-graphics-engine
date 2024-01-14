#version 330

in vec3 frag_color;
in vec2 frag_text_coord;

out vec4 color;

uniform sampler2D text_texture;
uniform int textured;
uniform vec3 in_color;
uniform float in_color_transparency;

void main() {
	color = vec4(in_color, in_color_transparency);

	if (textured == 1) {
		color = texture(text_texture, frag_text_coord);

		if (in_color_transparency > 0) {
			color = vec4(mix(in_color, color.xyz, color.a), 1);
		}
	}
}
