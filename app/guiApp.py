# -*- coding: utf-8 -*-
import wx
from Layout.singleCanvas import *
from opengl.WxGLScene import *

class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(u'wxPython + pyOpenGL')
        self.window = MyWindow(None)
        self.scene = WxGLScene(self.window.canvas)
        self.window.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
