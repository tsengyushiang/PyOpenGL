vertex_shader =\
    '''
#version 120

uniform float fx;
uniform float fy;
uniform float ppx;
uniform float ppy;
uniform float h;
uniform float w;

uniform vec3 offset;
uniform mat4 extrinct;

varying vec3 pos;
varying vec2 uv;

void main() {

    vec4 offsetPos = extrinct * (gl_Vertex-vec4(offset.xyz,0.0));
    gl_Position =  gl_ModelViewProjectionMatrix *offsetPos;

    pos = offsetPos.xyz;
    uv = vec2(  
        (gl_Vertex.x/gl_Vertex.z*fx+ppx)/w,
        (gl_Vertex.y/gl_Vertex.z*fy+ppy)/h
    );
}
'''
fragment_shader =\
    '''
#version 120

varying vec2 uv;
uniform sampler2D texColor;
uniform sampler2D texDepth;

varying vec3 pos;
uniform vec3 bboxPos;
uniform vec3 bboxNeg;

void main() {

    vec4 outbbox= vec4(0,0,0,0);
    if(pos.x>bboxPos.x || pos.y>bboxPos.y || pos.z>bboxPos.z){
       outbbox= vec4(0.5,0,0,0);
    }
    if(pos.x<bboxNeg.x || pos.y<bboxNeg.y || pos.z<bboxNeg.z){
       outbbox= vec4(0.5,0,0,0);
    }

    gl_FragColor = texture2D(texColor,uv)+outbbox;
    
}
'''
