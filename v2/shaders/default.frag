#version 330

in vec3 frag_normal;
in vec4 frag_color;
in float frag_transparency;
in vec3 frag_position;

out vec4 color;

uniform vec3 light_position = vec3(8, 8, 8);
uniform vec3 ambient_color = vec3(0.2, 0.2, 0.2);
uniform vec3 diffuse_color = vec3(1, 1, 1);

void main() {
    vec3 normal = normalize(frag_normal);

    vec3 light_direction = normalize(frag_position - light_position);
    float diffuse_intensity = max(dot(normal, light_direction), 0.0);

    vec3 ambient_light = ambient_color * frag_color.rgb;
    vec3 diffuse_light = diffuse_color * frag_color.rgb * diffuse_intensity;
    vec3 final_color = ambient_light + diffuse_light;

    // gamma correction
    final_color = pow(final_color, vec3(1.0 / 2.2));

    color = vec4(final_color, frag_transparency);
}
