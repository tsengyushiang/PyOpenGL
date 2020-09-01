# -*- coding: utf-8 -*-
from wxLayout.singleCanvas import *
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

        self.scene = WxGLScene(self.window.canvas)
        self.initObj()

        self.window.Show()
        return True

    def initObj(self):
        # read shader
        mat = ShaderMaterial(myShader.vertex_shader,
                             myShader.fragment_shader)
        # read obj file
        geo = Geometry(args.model)
        mesh = Mesh(mat, geo)
        # read texture
        texture = Texture(args.texture)
        self.scene.add(mesh)

if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
