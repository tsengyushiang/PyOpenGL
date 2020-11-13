vertex_shader =\
    '''
#version 120

varying vec2 tex_coord;
varying vec4 color;
void main() {
    vec2 scaledUV = gl_MultiTexCoord0.st*2.0-vec2(1.0,1.0);
    gl_Position = vec4(scaledUV.st,0.0,1.0);
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
    gl_FragColor = texture2D(tex1,tex_coord);
}
'''
