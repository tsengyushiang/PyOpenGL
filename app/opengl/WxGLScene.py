import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
from .Camera import *


class WxGLScene(glcanvas.GLCanvas):
    """GL 場景類 """

    def __init__(self, parent):
        """ 構造函數

        parent      - 父級窗口對象
        eye         - 觀察者的位置（默認 z 軸的正方向）
        up          - 對觀察者而言的上方（默認 y 軸的正方向）
        view        - 視景體
        """

        glcanvas.GLCanvas.__init__(self, parent, -1, style=glcanvas.WX_GL_RGBA |
                                   glcanvas.WX_GL_DOUBLEBUFFER | glcanvas.WX_GL_DEPTH_SIZE)

        self.parent = parent                                    # 父級窗口對象

        self.size = self.GetClientSize()                        # OpenGL 窗口的大小
        self.context = glcanvas.GLContext(self)                 # OpenGL 上下文
        self.mpos = None                                        # 鼠標位置
        self.initGL()                                           # 畫布初始化
        self.resize()
        self.meshes = []

        # 綁定窗口尺寸改變事件
        self.parent.Bind(wx.EVT_SIZE, self.onResize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onErase)        # 綁定背景擦除事件
        self.Bind(wx.EVT_PAINT, self.onPaint)                   # 綁定重繪事件

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)            # 綁定鼠標左鍵按下事件
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)                # 綁定鼠標左鍵彈起事件
        self.Bind(wx.EVT_RIGHT_UP, self.onRightUp)              # 綁定鼠標右鍵彈起事件
        self.Bind(wx.EVT_MOTION, self.onMouseMotion)            # 綁定鼠標移動事件
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)         # 綁定鼠標滾輪事件

    def resize(self):
        W, H = self.parent.GetSize()
        self.SetSize((W, H))
        self.SetCurrent(self.context)
        self.size = self.GetClientSize()
        self.camera.setViewport(W, H)

    def onResize(self, evt):
        """ 響應窗口尺寸改變事件 """

        if self.context:
            self.resize()
            self.Refresh(False)

        evt.Skip()

    def onErase(self, evt):
        """ 響應背景擦除事件 """

        pass

    def onPaint(self, evt):
        """ 響應重繪事件 """

        self.SetCurrent(self.context)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # 清除屏幕及深度緩存
        self.drawGL()                                       # 繪圖
        self.SwapBuffers()                                  # 切換緩衝區，以顯示繪製內容
        evt.Skip()

    def onLeftDown(self, evt):
        """ 響應鼠標左鍵按下事件 """
        self.CaptureMouse()
        self.mpos = evt.GetPosition()

    def onLeftUp(self, evt):
        """ 響應鼠標左鍵彈起事件 """
        try:
            self.ReleaseMouse()
        except:
            pass

    def onRightUp(self, evt):
        """ 響應鼠標右鍵彈起事件 """
        pass

    def onMouseMotion(self, evt):
        """ 響應鼠標移動事件 """
        if evt.Dragging() and evt.LeftIsDown():
            pos = evt.GetPosition()
            try:
                dx, dy = pos - self.mpos
            except:
                return
            self.mpos = pos
            self.camera.dragCamera(dx, -dy)
            self.Refresh(False)

    def activate(self):
        self.SetCurrent(self.context)

    def onMouseWheel(self, evt):
        """ 響應鼠標滾輪事件 """
        self.camera.zoom(evt.WheelRotation)
        self.Refresh(False)

    def initGL(self):
        """ 初始化 GL"""

        self.SetCurrent(self.context)

        # 設置畫布背景色
        glClearColor(0, 0, 0, 0)
        # 開啓深度測試，實現遮擋關係
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)                                      # 設置深度測試函數
        # GL_SMOOTH(光滑着色)/GL_FLAT(恆定着色)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_BLEND)                                          # 開啓混合
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)           # 設置混合函數
        # 啓用 Alpha 測試
        glEnable(GL_ALPHA_TEST)
        # 設置 Alpha 測試條件爲大於 0.05 則通過
        glAlphaFunc(GL_GREATER, 0.05)
        # 設置逆時針索引爲正面（GL_CCW/GL_CW）
        glFrontFace(GL_CW)
        glEnable(GL_LINE_SMOOTH)                                    # 開啓線段反走樣
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        self.camera = Camera(self.size[0], self.size[1])

    def add(self, mesh):
        self.meshes.append(mesh)

    def drawGL(self):
        """ 繪製 """

        # 清除屏幕及深度緩存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 設置視口
        self.camera.update()
        for mesh in self.meshes:
            mesh.draw()
