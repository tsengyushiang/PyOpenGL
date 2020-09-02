# -*- coding: utf-8 -*-
from wxLayout.fourCanvas import *
from opengl.WxGLScene import *
from opengl.GlutScene import *
from opengl.Geometry import *
from opengl.Texture import *
from opengl.ShaderMaterial import *
from opengl.Mesh import *
from opengl.Uniform import *

import shaders.texture2D as myShader

from Args.singleModelAndTexture import build_argparser
args = build_argparser().parse_args()


class mainApp(wx.App):
    def OnInit(self):
        self.window = MyWindow(None)

        self.window.SetTitle(u'wxPython + pyOpenGL')

        self.scene = WxGLScene(self.window.topleft)
        self.scene2 = WxGLScene(self.window.topright)

        self.initObj()

        self.window.Show()
        return True

    def initObj(self):

        # uniform
        tex = Texture(args.texture)
        tex2 = Texture('./medias/chess.png')

        uniform = Uniform()
        uniform.addTexture('tex', tex)
        uniform.addTexture('tex2', tex2)

        # read shader
        mat = ShaderMaterial(myShader.vertex_shader,
                             myShader.fragment_shader,
                             uniform)

        # read obj file
        geo = Geometry(args.model)

        mesh = Mesh(mat, geo)
        
        self.scene.add(mesh)
        self.scene2.add(mesh)


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
