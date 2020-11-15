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
uniform sampler2D depthMap;
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
    vec3 unTransNormalized = (inverTransMat* normalizeMat * vec4(position.xyz,1.0)).xyz;
    vec3 unTrans = (inverTransMat* vec4(position.xyz,1.0)).xyz;
    float u = (unTrans.x/unTrans.z*fx+ppx)/w;
    float v = (unTrans.y/unTrans.z*fy+ppy)/h;
    return vec3(u,v,unTransNormalized.z);
}

void main() {

    vec3 camDirection = position - cam_pose;
    vec3 uv = getProjectedUv(inverTransMat,position);    
    
    if (dot(camDirection, normal)<0){       

        if (uv.z - texture2D(depthMap,uv.xy).x<1e-2){
            gl_FragColor = texture2D(projectTex,uv.xy);
        }else{
            gl_FragColor = vec4(0.0,0.0,0.0,0.0);
        }
    }
    else{
        gl_FragColor = vec4(0.0,0.0,0.0,0.0);
    }
}
'''
