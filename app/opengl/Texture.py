from OpenGL.GL import *


class Texture:
    def __init__(self, imageName):
        """Load an image from a file using PIL.
        This is closer to what you really want to do than the
        original port's crammed-together stuff that set global
        state in the loading method.  Note the process of binding
        the texture to an ID then loading the texture into memory.
        This didn't seem clear to me somehow in the tutorial.
        """
        try:
            from PIL.Image import open
        except ImportError:
            from Image import open
        im = open(imageName)
        im = im.convert("RGBA")
        try:
            ix, iy, image = im.size[0], im.size[1], im.tobytes(
                "raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tobytes(
                "raw", "RGBX", 0, -1)
        # generate a texture ID
        self.id = glGenTextures(1)
        # make it current
        glBindTexture(GL_TEXTURE_2D, self.id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # copy the texture into the current texture ID
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, image)
        print('load texture success : '+imageName, ix, iy)
        # glGenerateMipmap(GL_TEXTURE_2D)
