vertex_shader =\
    '''
#version 120
uniform mat4 normalizeMat;
varying vec3 position;

uniform mat4 inverTransMat;
uniform float ppx;
uniform float ppy;
uniform float fx;
uniform float fy;
uniform float w;
uniform float h;
varying float z;

vec3 getProjectedUv(mat4 inverTransMat,vec3 position){ 
    vec3 unTransNormalized = (normalizeMat* inverTransMat * vec4(position.xyz,1.0)).xyz;
    vec3 unTrans = (inverTransMat* vec4(position.xyz,1.0)).xyz;
    float u = (unTrans.x/unTrans.z*fx+ppx)/w;
    float v = (unTrans.y/unTrans.z*fy+ppy)/h;
    return vec3(u,v,unTransNormalized.z);
}

void main() {
    
    vec3 scaledUV = getProjectedUv(inverTransMat,gl_Vertex.xyz);
    gl_Position = vec4(scaledUV*2.0-1.0,1.0);
    position = gl_Vertex.xyz;
}
'''
fragment_shader =\
    '''
#version 120
uniform mat4 normalizeMat;
varying vec3 position;
uniform mat4 inverTransMat;
uniform float ppx;
uniform float ppy;
uniform float fx;
uniform float fy;
uniform float w;
uniform float h;
varying float z;

vec3 getProjectedUv(mat4 inverTransMat,vec3 position){ 
    vec3 unTransNormalized = (normalizeMat* inverTransMat * vec4(position.xyz,1.0)).xyz;
    vec3 unTrans = (inverTransMat* vec4(position.xyz,1.0)).xyz;
    float u = (unTrans.x/unTrans.z*fx+ppx)/w;
    float v = (unTrans.y/unTrans.z*fy+ppy)/h;
    return vec3(u,v,unTransNormalized.z);
}

void main() {    
    vec3 uv = getProjectedUv(inverTransMat,position);
    gl_FragColor = vec4(uv.z,uv.z,uv.z,1.0);
}
'''
