#version 330

in vec3 frag_normal;
in vec4 frag_color;
in float frag_transparency;
in vec3 frag_position;
in vec2 frag_texture_coords;

out vec4 color;

uniform vec3 light_position = vec3(0, 64, 0);
uniform vec3 ambient_color = vec3(0.5, 0.5, 0.5);
uniform vec3 diffuse_color = vec3(1, 1, 1);
// material data
uniform bool border_only;
uniform float border_size;
uniform vec3 border_color;

vec4 withBorder(bool border_only, float border_size, vec3 border_color, vec4 final_color) {
    if (
        frag_texture_coords.x < border_size
        || frag_texture_coords.x > 1.0 - border_size
        || frag_texture_coords.y < border_size
        || frag_texture_coords.y > 1.0 - border_size
    ) {
        return vec4(border_color, frag_transparency);
    }

    return vec4(final_color.xyz, border_only == true ? 0 : final_color.w);
}

void main() {
    vec3 normal = normalize(frag_normal);

    vec3 light_direction = normalize(frag_position - light_position);
    float diffuse_intensity = max(dot(normal, light_direction), 0.0);

    vec3 ambient_light = ambient_color * frag_color.rgb;
    vec3 diffuse_light = diffuse_color * frag_color.rgb * diffuse_intensity;
    vec3 final_color = ambient_light + diffuse_light;

    // gamma correction
    color = vec4(pow(final_color, vec3(1.0 / 2.2)), frag_transparency);

    // border modification
    color = withBorder(border_only, border_size, border_color, color);
}
