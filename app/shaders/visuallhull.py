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

vec3 pixel2point(vec2 pixel,float depthValue){
    float x = (pixel.x-ppx)/fx;
    float y = (pixel.y-ppy)/fy;
    return vec3(x*depthValue,y*depthValue,depthValue);
}

vec2 point2pixel(vec3 point,float depthValue){
    float u = (point.x/depthValue*fx+ppx)/w;
    float v = (point.y/depthValue*fy+ppy)/h;
    return vec2(u,v);
}

void main() {
    
    float z = ((gl_VertexID/(vL*vL)))/vL;
    float zRemain = mod(gl_VertexID,vL*vL);
    // 0~vL
    float y = vL -zRemain/vL;
    // 0~vL
    float x = mod(zRemain,vL);

    vec2 pixel = vec2(x/vL*w,y/vL*h);
    vec3 projectPoint = pixel2point(pixel,depthValue);
    
    vec3 point = vec3(x/vL-0.5,y/vL-0.5,z);

    vec3 renderPoint = point;
    vec2 unprojectPixel = point2pixel(renderPoint,depthValue);
    
    /*
    vec3 point = vec3(x/vL,y/vL,z);
    vec2 pixel = point2pixel(point,depthValue);
    */

    depthTest = (z>projectPoint.z && projectPoint.z>0) ? 0:1;
    gl_Position =  gl_ModelViewProjectionMatrix *vec4(renderPoint.xy,z,1.0);
    uv1 = unprojectPixel;
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

    if(color2.x>1e-05 && uv1.x>0 && uv1.y>0 && uv1.y<1.0 && uv1.x<1.0){
        if( depthTest==0){
            gl_FragColor = color1;
        }else{
            gl_FragColor = vec4(0.0,1.0,0.0,1.0);
        }
    }
    else{
        gl_FragColor = vec4(uv1.xy,0.0,0.0);
    }
}
'''
