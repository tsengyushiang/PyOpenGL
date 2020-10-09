vertex_shader =\
    '''
#version 130

uniform mat4 normalizeMat;

varying vec3 color;

varying vec3 normal;
varying vec3 fragPos;

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * normalizeMat * gl_Vertex;
    fragPos = (gl_ModelViewMatrix * gl_Vertex).xyz;
    normal = gl_Color.xyz;
    color = vec3(1.0,1.0,1.0);
}
'''
fragment_shader =\
    '''
#version 130

varying vec3 color;

vec3 lightColor = vec3(0.3,0.3,0.3);

// ambient light
float ambientStrength = 1.0;

// diffuse light
varying vec3 normal;
varying vec3 fragPos;
vec3 lightPos=vec3(0.5,0.5,0.5);

// specular light
uniform vec3 viewPos;
float specularStrength = 0.5;

void main() {

    // ambient light
    vec3 ambient = ambientStrength * lightColor;

    // diffuse light
    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPos - fragPos);  
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // specular light
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;        

    vec3 result = (ambient + diffuse + specular) * color;
    gl_FragColor = vec4(result, 1.0);
}
'''
