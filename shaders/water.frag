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

float random(float x) {
	return fract(sin(x) * 10000);
}

float noise(vec2 p) {
	return random(p.x + p.y * 10000);
}

vec2 sw(vec2 p) { return vec2(floor(p.x), floor(p.y)); }
vec2 se(vec2 p) { return vec2(ceil(p.x), floor(p.y)); }
vec2 nw(vec2 p) { return vec2(floor(p.x), ceil(p.y)); }
vec2 ne(vec2 p) { return vec2(ceil(p.x), ceil(p.y)); }

float smoothNoise(vec2 p) {
	vec2 interp = smoothstep(0, 1, fract(p));
	float s = mix(noise(sw(p)), noise(se(p)), interp.x);
	float n = mix(noise(nw(p)), noise(ne(p)), interp.x);
	return mix(s, n, interp.y);
}

float fractalNoise(vec2 p) {
	float x = 0;
	x += smoothNoise(p);
	x += smoothNoise(p * 2) / 2;
	x /= 1 + 1 / 2;
	return x;
}

float movingNoise(vec2 p) {
	float time = elapsed_time / 3000;
	float x = fractalNoise(p + time);
	float y = fractalNoise(p - time);
	return fractalNoise(p + vec2(x, y));
}

float nestedNoise(vec2 p) {
	float x = movingNoise(p);
	float y = movingNoise(p + 100);
	return movingNoise(p + vec2(x, y));
}

float roundToDecimal(float value, float decimalPlace) {
	float multiplier = pow(10.0, decimalPlace);
	return round(value * multiplier) / multiplier;
}

void main() {
	vec3 normal = normalize(frag_normal);

	vec3 light_direction = normalize(frag_position - light_position);
	float diffuse_intensity = max(dot(normal, light_direction), 0.0);

	vec3 ambient_light = ambient_color * frag_color.rgb;
	vec3 diffuse_light = diffuse_color * frag_color.rgb * diffuse_intensity;
	vec3 final_color = ambient_light + diffuse_light;

	final_color = vec3(pow(final_color, vec3(1.0 / 2.2)));

	// vec2 uv = vec2(frag_position.x, frag_position.z);
	vec2 uv = vec2(roundToDecimal(frag_position.x - 0.5, 0), roundToDecimal(frag_position.z - 0.5, 0));

	float n = 0.3 * nestedNoise(uv);

	color = vec4(mix(vec3(final_color.rgb), vec3(final_color.rgb) * 0.5, n), frag_transparency);
}
