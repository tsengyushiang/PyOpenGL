vertex_shader =\
    '''
#version 120

uniform float fx;
uniform float fy;
uniform float ppx;
uniform float ppy;
uniform float h;
uniform float w;

uniform float maxdepth=100;
uniform float mindepth=0;

varying vec4 color;
varying vec2 uv;

void main() {
    
    if(gl_Vertex.z>maxdepth){
        gl_Position=vec4(0.0,0.0,0.0,1.0);
    }else{
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        color = gl_Vertex;
    }

    uv = vec2(
        (gl_Vertex.x/gl_Vertex.z*fx+ppx)/w,
        (gl_Vertex.y/gl_Vertex.z*fy+ppy)/h
    );
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
