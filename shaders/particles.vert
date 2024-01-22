#version 330

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 in_position;
in vec4 in_color;

out vec4 color;

vec4 perform_frustum_culling(vec4 position) {
    vec4 v_position = projection * view * model * vec4(in_position, 1.0);
    // to render edges of screen (near camera plane)
    float offset = -5;

    // is vertex in camera view?
    if (abs(v_position.x) + offset <= v_position.w && abs(v_position.y) + offset <= v_position.w && v_position.z >= 0.0 && v_position.z + offset <= v_position.w) {
        return v_position;
    }

    // offscreen coordinates are discarted
    return vec4(2.0, 2.0, 2.0, 1.0);
}

void main() {
    gl_Position = perform_frustum_culling(vec4(in_position, 1.0));
    color = in_color;
}
