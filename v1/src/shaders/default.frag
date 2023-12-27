#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 coords;
in vec3 color;
in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
uniform float transparency;
uniform float borderSize;
uniform vec3 borderColor;

uniform bool fogEnabled = false;

vec3 getLight(vec3 targetColor) {
    vec3 Normal = normalize(normal);

    // ambient
    vec3 ambient = light.Ia;

    // diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // specular
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return targetColor * (ambient + diffuse + specular);
}

vec3 addBorder(vec3 originalColor) {
    float maxX = 1.0 - borderSize;
    float minX = borderSize;
    float maxY = maxX;
    float minY = minX;

    if (!(coords.x < maxX && coords.x > minX && coords.y < maxY && coords.y > minY)) {
        return vec3(borderColor);
    }
    return originalColor;
}

float getFogFactor(float d) {
    if (!fogEnabled) {
        return 0;
    }

    const float FogMax = 32.0;
    const float FogMin = 24.0;

    if (d >= FogMax) return 1;
    if (d <= FogMin) return 0;

    return 1 - (FogMax - d) / (FogMax - FogMin);
}

void main() {
    float gamma = 2.2;

    vec3 finalColor = color;
    vec3 textureColor = texture(u_texture_0, uv_0).rgb;
    if (length(textureColor) != 0) {
        finalColor = textureColor;
    }

    // texture gamma correction
    finalColor = pow(finalColor, vec3(gamma));
    // apply light
    finalColor = getLight(finalColor);
    // actual gamma correction
    finalColor = pow(finalColor, 1 / vec3(gamma));

    float d = distance(camPos, fragPos);
    float alpha = getFogFactor(d);

    // fragColor = vec4(addBorder(finalColor), transparency);
    fragColor = vec4(mix(addBorder(finalColor), vec3(1, 1, 1), alpha), alpha + transparency);
}
