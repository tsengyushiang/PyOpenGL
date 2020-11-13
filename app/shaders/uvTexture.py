vertex_shader =\
    '''
#version 120
uniform mat4 normalizeMat;
varying vec2 tex_coord ;
void main() {
    gl_Position = vec4(gl_MultiTexCoord0.s*2.0-1.0,gl_MultiTexCoord0.t*2.0-1.0,0.0,1.0);
    tex_coord  = gl_MultiTexCoord0.st;
}
'''
fragment_shader =\
    '''
#version 120

varying vec2 tex_coord ;
void main() {
    gl_FragColor = vec4(tex_coord,1.0,1.0);
}
'''
