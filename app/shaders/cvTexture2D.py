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
uniform sampler2D texColor;
uniform sampler2D texDepth;

void main() {
    if(color.z>0.5){
        gl_FragColor = texture2D(texColor,uv);
    }else{
        gl_FragColor = texture2D(texDepth,uv);
    }
}
'''
