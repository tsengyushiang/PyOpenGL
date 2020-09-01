# -*- coding: utf-8 -*-
from wxLayout.fourCanvas import *
from opengl.WxGLScene import *
from opengl.GlutScene import *
from opengl.Geometry import *
from opengl.Texture import *
from opengl.ShaderMaterial import *
from opengl.Mesh import *

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

        # read shader
        self.scene.activate()
        mat = ShaderMaterial(myShader.vertex_shader,
                             myShader.fragment_shader)

        # read texture
        texture = Texture(args.texture)

        self.scene2.activate()
        mat2 = ShaderMaterial(myShader.vertex_shader,
                              myShader.fragment_shader)

        # read texture
        texture2 = Texture(args.texture)

        # read obj file
        geo = Geometry(args.model)
        geo2 = Geometry(args.model)


        mesh = Mesh(mat, geo)
        mesh2 = Mesh(mat2, geo2)

        self.scene.add(mesh)
        self.scene2.add(mesh2)


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
