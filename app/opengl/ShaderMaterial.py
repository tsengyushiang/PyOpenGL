from OpenGL.GL import *
from OpenGL.GL import shaders


class ShaderMaterial():
    def __init__(self, vert, frag):
        # init shader
        try :
            VERTEX_SHADER = shaders.compileShader(
                vert, GL_VERTEX_SHADER)
            FRAGMENT_SHADER = shaders.compileShader(
                frag, GL_FRAGMENT_SHADER)
            self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        except :
            print('Compile shader after glutContext create. Init GlutScene first')

    def activate(self):
        # use shader
        shaders.glUseProgram(self.shader)

    def deactivate(self):
        shaders.glUseProgram(0)
