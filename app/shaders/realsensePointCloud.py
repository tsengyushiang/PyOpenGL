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

uniform vec3 maker1;
uniform mat4 extrinct;

varying vec3 pos;
varying vec2 uv;

void main() {
    
    if(gl_Vertex.z>maxdepth){
        gl_Position=vec4(0.0,0.0,0.0,1.0);
    }else{
        gl_Position = gl_ModelViewProjectionMatrix * extrinct * (gl_Vertex-vec4(maker1.xyz,0.0));
    }

    pos = gl_Vertex.xyz;
    uv = vec2(  
        (gl_Vertex.x/gl_Vertex.z*fx+ppx)/w,
        (gl_Vertex.y/gl_Vertex.z*fy+ppy)/h
    );
}
'''
fragment_shader =\
    '''
#version 120

varying vec3 pos;
varying vec2 uv;
uniform sampler2D texColor;
uniform sampler2D texDepth;

uniform vec3 maker1;
uniform vec3 maker2;

void main() {

    if(distance(pos,maker1)<0.03){
        gl_FragColor = vec4(1.0,0.0,0.0,1.0);
        return;
    }
    
    if(distance(pos,maker2)<0.03){
        gl_FragColor = vec4(0.0,1.0,0.0,1.0);
        return;
    }
    
    gl_FragColor = texture2D(texColor,uv);
    
}
'''
