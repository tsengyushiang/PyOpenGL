vertex_shader =\
    '''
#version 120
uniform mat4 normalizeMat;

varying vec2 tex_coord;
varying vec3 normal;
varying vec3 position;

void main() {
    gl_Position = gl_ModelViewProjectionMatrix * normalizeMat * gl_Vertex;
    normal = gl_Color.xyz;
    tex_coord = gl_MultiTexCoord0.st;
    position = gl_Vertex.xyz;
}
'''
fragment_shader =\
    '''
#version 120

uniform mat4 normalizeMat;
uniform sampler2D projectTex;
uniform sampler2D tex1;
varying vec2 tex_coord;

varying vec3 normal;
varying vec3 position;

uniform vec3 cam_pose;
uniform mat4 inverTransMat;

uniform float ppx;
uniform float ppy;
uniform float fx;
uniform float fy;
uniform float w;
uniform float h;

vec3 getProjectedUv(mat4 inverTransMat,vec3 position){    
    vec3 unTrans = (inverTransMat* normalizeMat * vec4(position.xyz,1.0)).xyz;
    float u = (unTrans.x/unTrans.z*fx+ppx)/w;
    float v = (unTrans.y/unTrans.z*fy+ppy)/h;
    return vec3(u,v,unTrans.z);
}

void main() {

    vec3 camDirection = position - cam_pose;
    vec3 uv = getProjectedUv(inverTransMat,position);

    gl_FragColor = vec4(uv.z,uv.z,uv.z,uv.z>=1.0? 0.0:1.0);

    /*
    if (dot(camDirection, normal)>0){
        gl_FragColor = vec4(0.0,0.0,0.0,0.0);
    }
    else{
        vec3 uv = getProjectedUv(inverTransMat,position);
        gl_FragColor = texture2D(projectTex,uv.xy);
    }
    */
}
'''
