vertex_shader =\
    '''
#version 120

varying vec4 color;
varying vec2 uv;
void main() {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    color = gl_Color;
    uv = vec2(gl_Vertex.x,gl_Vertex.y)*0.5f+0.5f;
}
'''
fragment_shader =\
    '''
#version 120

varying vec4 color;
varying vec2 uv;
uniform sampler2D tex;
uniform sampler2D tex2;

void main() {
    if(color.z>0.5){
        gl_FragColor = texture2D(tex,uv)+vec4(1.0,1.0,0.0,1.0);
    }else{
        gl_FragColor = texture2D(tex2,uv)+vec4(1.0,0.0,0.0,1.0);
    }
}
'''
