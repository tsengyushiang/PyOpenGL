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

varying vec3 pos;
varying vec2 uv;

vec3 pixel2point(vec2 pixel,float depthValue){
    float x = (pixel.x-ppx)/fx;
    float y = (pixel.y-ppy)/fy;
    return vec3(x*depthValue,y*depthValue,depthValue);
}

void main() {

    float x = mod(gl_VertexID,w);
    float y = h-gl_VertexID/w;

    vec2 pixel = vec2(x,y);

    vec3 point = pixel2point(pixel,depthValue);
    
    vec4 offsetPos = extrinct * vec4(point.xyz,1.0);
    gl_Position =  gl_ModelViewProjectionMatrix *offsetPos;

    pos = offsetPos.xyz;
    uv = vec2(x/w,y/h);
}
'''
fragment_shader =\
    '''
#version 130

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
