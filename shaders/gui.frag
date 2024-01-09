#version 330

in vec3 frag_color;
in vec2 frag_text_coord;

out vec4 color;

uniform sampler2D text_texture;
uniform int textured;
uniform vec3 in_color;

void main() {
    color = vec4(in_color, 1.0);

    if (textured == 1) {
        color = texture(text_texture, frag_text_coord);
        color = vec4(mix(in_color, color.xyz, color.a), 1);
    }
}
