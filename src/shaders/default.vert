#version 330 core

layout (location = 0) in vec2 in_textcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 coords;
out vec3 color;
out float borderSize;
out vec3 borderColor;
out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

uniform vec3 in_color;
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    coords = in_textcoord_0;
    color = in_color;
    uv_0 = in_textcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);

    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}
