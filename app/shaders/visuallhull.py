vertex_shader =\
    '''
#version 130

uniform float fx;
uniform float fy;
uniform float ppx;
uniform float ppy;

uniform float h;
uniform float w;
uniform float d;

uniform mat4 extrinct1;
uniform mat4 extrinct2;

attribute float depthValue;

void main() {

    float x = mod(gl_VertexID,w*h);
    float y = mode(x,h);
    float z = x/h;
    
    gl_Position =  gl_ModelViewProjectionMatrix *vec4(x,y,z,1.0);

}
'''
fragment_shader =\
    '''
#version 130

uniform sampler2D texDepth1;
uniform sampler2D texDepth2;

void main() {   

    gl_FragColor = vec4(1.0,0.0,0.0,1.0);
    
}
'''
