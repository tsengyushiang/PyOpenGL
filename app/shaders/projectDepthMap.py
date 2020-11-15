vertex_shader =\
    '''
#version 120

varying vec2 uv;

uniform mat4 normalizeMat;
uniform mat4 inverTransMat;
uniform float ppx;
uniform float ppy;
uniform float fx;
uniform float fy;
uniform float w;
uniform float h;

vec2 getProjectedUv(mat4 inverTransMat,vec3 position){
    vec3 unTrans = (inverTransMat* vec4(position.xyz,1.0)).xyz;
    float u = (unTrans.x/unTrans.z*fx+ppx)/w;
    float v = (unTrans.y/unTrans.z*fy+ppy)/h;
    return vec2(u,v);
}

void main() {
    
    vec2 scaledUV = getProjectedUv(inverTransMat,gl_Vertex.xyz);
    gl_Position = vec4(scaledUV.st*2.0-1.0,0.0,1.0);
    uv = scaledUV;
}
'''
fragment_shader =\
    '''
#version 120

uniform sampler2D projectTex;
varying vec2 uv;

void main() {
    gl_FragColor = texture2D(projectTex,uv);
}
'''
