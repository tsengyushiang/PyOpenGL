from OpenGL.GL import *
from OpenGL.GL import shaders


class Uniform:
    def __init__(self):
        pass
        self.dict = []
        self.textures = []

    def init(self):
        for texture in self.textures:
            texture[1].init()

    def addTexture(self, name, texture):
        self.textures.append([name, texture])
