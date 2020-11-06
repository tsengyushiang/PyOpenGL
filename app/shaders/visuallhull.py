vertex_shader =\
    '''
#version 130

uniform float fx;
uniform float fy;
uniform float ppx;
uniform float ppy;
uniform float w;
uniform float h;

uniform float vL;
uniform float scale;

uniform mat4 extrinct1;
uniform mat4 extrinct2;


attribute float depthValue;
varying float depthTest;
varying vec2 uv1;
varying vec2 uv2;

vec3 pixel2point(vec2 pixel,float depthValue,float z){
    float x = (pixel.x-ppx)/fx;
    float y = (pixel.y-ppy)/fy;
    return vec3(x*depthValue,y*depthValue,z);
}

vec2 point2pixel(vec3 point,float depthValue){
    float u = (point.x/depthValue*fx+ppx);
    float v = (point.y/depthValue*fy+ppy);
    return vec2(u,v);
}

void main() {
    
    float z = ((gl_VertexID/(vL*vL)))/vL;
    float y = (mod(gl_VertexID,vL*vL)/vL)/vL+0.5;
    float x = (mod(mod(gl_VertexID,vL*vL),vL))/vL-0.5;
    vec3 point = vec3(x,1-y,z);
    vec2 pixel = point2pixel(point,depthValue);

    /*
    vec2 pixel = vec2(x*w,h-y*h);
    vec3 point = pixel2point(pixel,depthValue,z);
    gl_Position =  gl_ModelViewProjectionMatrix *vec4(point.xyz,1.0);

    depthTest = (z>depthValue && depthValue>0) ? 0:1;
    */

    depthTest = (z>depthValue && depthValue>0) ? 0:1;
    gl_Position =  gl_ModelViewProjectionMatrix *vec4(point.xyz,1.0);
    uv1 =vec2(pixel.x/w,pixel.y/h);
}
'''
fragment_shader =\
    '''
#version 130

uniform sampler2D texDepth1;
uniform sampler2D texDepth2;

varying float depthTest;
varying vec2 uv1;
varying vec2 uv2;

void main() {
    vec4 color1 = texture2D(texDepth1,uv1);
    vec4 color2 = texture2D(texDepth2,uv1);
    
    if(color2.x>1e-05 && depthTest==0 && uv1.x>0 && uv1.y>0 && uv1.y<1.0 && uv1.x<1.0){
        gl_FragColor = color1;
    }
    else{
        gl_FragColor = vec4(0.0,0.0,0.0,0.0);
    }
}
'''
