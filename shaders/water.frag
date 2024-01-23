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
uniform float elapsed_time = 0;
// material data
uniform bool border_only = false;
uniform float border_size = 0;
uniform vec3 border_color = vec3(0, 0, 0);

float hash(vec2 p)
{
	return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

float noise(vec2 p)
{
	vec2 i = floor(p);
	vec2 f = fract(p);

	vec2 u = f * f * (3.0 - 2.0 * f);

	return mix(mix(hash(i + vec2(0.0, 0.0)), hash(i + vec2(1.0, 0.0)), u.x),
	mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}

float smoothNoise(vec2 uv)
{
	float corners = (noise(uv + vec2(-1.0, -1.0)) + noise(uv + vec2(1.0, -1.0)) + noise(uv + vec2(-1.0, 1.0)) + noise(uv + vec2(1.0, 1.0))) / 16.0;
	float sides = (noise(uv + vec2(-1.0, 0.0)) + noise(uv + vec2(1.0, 0.0)) + noise(uv + vec2(0.0, -1.0)) + noise(uv + vec2(0.0, 1.0))) / 8.0;
	float center = noise(uv) / 4.0;

	return corners + sides + center;
}

float perlinNoise(vec2 p)
{
	return 0.5 + 0.5 * sin(10.0 * p.x + 10.0 * p.y + 0.1 * sin(5.0 * p.x + 5.0 * p.y));
}

void main() {
	vec3 waterColor = vec3(0.0, 1.0, 1.0);

	float time = elapsed_time / 1000;
	float frequency1 = 1.0;
	float frequency2 = 2.0;
	float amplitude1 = 0.1;
	float amplitude2 = 0.05;

	float wave1 = amplitude1 * sin(time * frequency1);
	float wave2 = amplitude2 * sin(time * frequency2);

	float displacement = wave1 + wave2;

	vec2 uv = vec2(frag_position.x, frag_position.z);
	uv.x += displacement * 10;

	float noise = (noise(uv * 10) - 0.5);

	vec3 finalColor = waterColor + vec3(noise);

	color = vec4(finalColor, 1);
}
