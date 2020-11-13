vertex_shader =\
    '''
#version 120
uniform mat4 normalizeMat;

varying vec2 tex_coord;
varying vec4 color;
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * normalizeMat * gl_Vertex;
    color = gl_Color;
    tex_coord = gl_MultiTexCoord0.st;
}
'''
fragment_shader =\
    '''
#version 120

uniform sampler2D tex1;
varying vec2 tex_coord;
varying vec4 color;
void main() {
    gl_FragColor = texture2D(tex1,tex_coord.st);
}
'''
