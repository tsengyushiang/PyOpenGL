vertex_shader =\
    '''
#version 120

varying vec4 color;
varying vec2 uv;
void main() {
    vec4 pos = vec4(
        gl_Vertex.x*gl_Vertex.z,
        gl_Vertex.y*gl_Vertex.z,
        1.0*gl_Vertex.z,
        1.0
    );
    gl_Position = gl_ModelViewProjectionMatrix * pos;
    color = gl_Vertex;
    uv = vec2(gl_Vertex.x,gl_Vertex.y);
}
'''
fragment_shader =\
    '''
#version 120

varying vec4 color;
varying vec2 uv;
uniform sampler2D texColor;
uniform sampler2D texDepth;

void main() {
    gl_FragColor = texture2D(texColor,uv);
}
'''
