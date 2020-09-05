from OpenGL.GL import *
from OpenGL.GL import shaders


class ShaderMaterial():
    def __init__(self, vert, frag, uniform):
        self.vertShader = vert
        self.fragShader = frag
        self.uniform = uniform

    def init(self):

        VERTEX_SHADER = shaders.compileShader(
            self.vertShader, GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader(
            self.fragShader, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(
            VERTEX_SHADER, FRAGMENT_SHADER)

        self.uniform.init()

    def activate(self):
        # use shader
        shaders.glUseProgram(self.shader)

        for texture in self.uniform.textures:
            location = glGetUniformLocation(self.shader, texture[0])
            glUniform1i(location, texture[1].id)

        for floatNum in self.uniform.floats:
            location = glGetUniformLocation(self.shader, floatNum[0])
            glUniform1f(location, floatNum[1])

    def deactivate(self):
        shaders.glUseProgram(0)
