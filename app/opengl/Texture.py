from OpenGL.GL import *
import numpy as np


class Texture:
    def __init__(self, input=None):
        """Load an image from a file using PIL.
        This is closer to what you really want to do than the
        original port's crammed-together stuff that set global
        state in the loading method.  Note the process of binding
        the texture to an ID then loading the texture into memory.
        This didn't seem clear to me somehow in the tutorial.
        """
        if(isinstance(input, str)):
            try:
                from PIL.Image import open
            except ImportError:
                from Image import open
            im = open(input)
            im = im.convert("RGBA")
            try:
                ix, iy, image = im.size[0], im.size[1], im.tobytes(
                    "raw", "RGBA", 0, -1)
            except SystemError:
                ix, iy, image = im.size[0], im.size[1], im.tobytes(
                    "raw", "RGBX", 0, -1)

            # generate a texture ID
            self.image = image
            self.ix = ix
            self.iy = iy
            self.type = GL_RGBA
            print('texture loaded : '+input)
        else:
            self.image = np.flipud(input)
            self.ix = input.shape[0]
            self.iy = input.shape[1]
            self.type = GL_BGR

    def init(self):
        # make it current
        self.id = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0+self.id)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # copy the texture into the current texture ID
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.iy, self.ix, 0,
                     self.type, GL_UNSIGNED_BYTE, self.image)

    def update(self, input):
        self.image = np.flipud(input)
        self.ix = input.shape[0]
        self.iy = input.shape[1]
        self.type = GL_BGR
        glDeleteTextures([self.id])
        self.init()
