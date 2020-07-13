vertex_shader=\
'''
#version 120

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
'''
fragment_shader=\
'''
#version 120

void main() {
    gl_FragColor = vec4( 0, 1, 0, 1 );
}
'''