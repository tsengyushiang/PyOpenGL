import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *

class WxGLScene(glcanvas.GLCanvas):
    """GL 場景類 """

    def __init__(self, parent, eye=[0, 0, 5], aim=[0, 0, 0], up=[0, 1, 0], view=[-1, 1, -1, 1, 3.5, 10]):
        """ 構造函數

        parent      - 父級窗口對象  
        eye         - 觀察者的位置（默認 z 軸的正方向）  
        up          - 對觀察者而言的上方（默認 y 軸的正方向）  
        view        - 視景體  
        """

        glcanvas.GLCanvas.__init__(self, parent, -1, style=glcanvas.WX_GL_RGBA |
                                   glcanvas.WX_GL_DOUBLEBUFFER | glcanvas.WX_GL_DEPTH_SIZE)

        self.parent = parent                                    # 父級窗口對象
        self.eye = eye                                          # 觀察者的位置
        self.aim = aim                                          # 觀察目標（默認在座標原點）
        self.up = up                                            # 對觀察者而言的上方
        self.view = view                                        # 視景體

        self.size = self.GetClientSize()                        # OpenGL 窗口的大小
        self.context = glcanvas.GLContext(self)                 # OpenGL 上下文
        self.zoom = 1.0                                         # 視口縮放因子
        self.mpos = None                                        # 鼠標位置
        self.initGL()                                           # 畫布初始化

        # 綁定窗口尺寸改變事件
        self.parent.Bind(wx.EVT_SIZE, self.onResize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onErase)        # 綁定背景擦除事件
        self.Bind(wx.EVT_PAINT, self.onPaint)                   # 綁定重繪事件

        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)            # 綁定鼠標左鍵按下事件
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)                # 綁定鼠標左鍵彈起事件
        self.Bind(wx.EVT_RIGHT_UP, self.onRightUp)              # 綁定鼠標右鍵彈起事件
        self.Bind(wx.EVT_MOTION, self.onMouseMotion)            # 綁定鼠標移動事件
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)         # 綁定鼠標滾輪事件

    def onResize(self, evt):
        """ 響應窗口尺寸改變事件 """

        if self.context:
            W, H = self.parent.GetSize()
            self.SetSize((W, H))
            self.SetCurrent(self.context)
            self.size = self.GetClientSize()
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

            # 限於篇幅省略改變觀察者位置的代碼

            self.Refresh(False)

    def onMouseWheel(self, evt):
        """ 響應鼠標滾輪事件 """

        if evt.WheelRotation < 0:
            self.zoom *= 1.1
            if self.zoom > 100:
                self.zoom = 100
        elif evt.WheelRotation > 0:
            self.zoom *= 0.9
            if self.zoom < 0.01:
                self.zoom = 0.01

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

    def drawGL(self):
        """ 繪製 """

        # 清除屏幕及深度緩存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 設置視口
        glViewport(0, 0, self.size[0], self.size[1])

        # 設置投影（透視投影）
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        k = self.size[0]/self.size[1]
        if k > 1:
            glFrustum(
                self.zoom*self.view[0]*k,
                self.zoom*self.view[1]*k,
                self.zoom*self.view[2],
                self.zoom*self.view[3],
                self.view[4], self.view[5]
            )
        else:
            glFrustum(
                self.zoom*self.view[0],
                self.zoom*self.view[1],
                self.zoom*self.view[2]/k,
                self.zoom*self.view[3]/k,
                self.view[4], self.view[5]
            )

        # 設置視點
        gluLookAt(
            self.eye[0], self.eye[1], self.eye[2],
            self.aim[0], self.aim[1], self.aim[2],
            self.up[0], self.up[1], self.up[2]
        )

        # 設置模型視圖
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # ---------------------------------------------------------------
        glBegin(GL_LINES)                    # 開始繪製線段（世界座標系）

        # 以紅色繪製 x 軸
        glColor4f(1.0, 0.0, 0.0, 1.0)        # 設置當前顏色爲紅色不透明
        glVertex3f(-0.8, 0.0, 0.0)           # 設置 x 軸頂點（x 軸負方向）
        glVertex3f(0.8, 0.0, 0.0)            # 設置 x 軸頂點（x 軸正方向）

        # 以綠色繪製 y 軸
        glColor4f(0.0, 1.0, 0.0, 1.0)        # 設置當前顏色爲綠色不透明
        glVertex3f(0.0, -0.8, 0.0)           # 設置 y 軸頂點（y 軸負方向）
        glVertex3f(0.0, 0.8, 0.0)            # 設置 y 軸頂點（y 軸正方向）

        # 以藍色繪製 z 軸
        glColor4f(0.0, 0.0, 1.0, 1.0)        # 設置當前顏色爲藍色不透明
        glVertex3f(0.0, 0.0, -0.8)           # 設置 z 軸頂點（z 軸負方向）
        glVertex3f(0.0, 0.0, 0.8)            # 設置 z 軸頂點（z 軸正方向）

        glEnd()                              # 結束繪製線段

        # ---------------------------------------------------------------
        glBegin(GL_TRIANGLES)                # 開始繪製三角形（z 軸負半區）

        glColor4f(1.0, 0.0, 0.0, 1.0)        # 設置當前顏色爲紅色不透明
        glVertex3f(-0.5, -0.366, -0.5)       # 設置三角形頂點
        glColor4f(0.0, 1.0, 0.0, 1.0)        # 設置當前顏色爲綠色不透明
        glVertex3f(0.5, -0.366, -0.5)        # 設置三角形頂點
        glColor4f(0.0, 0.0, 1.0, 1.0)        # 設置當前顏色爲藍色不透明
        glVertex3f(0.0, 0.5, -0.5)           # 設置三角形頂點

        glEnd()                              # 結束繪製三角形

        # ---------------------------------------------------------------
        glBegin(GL_TRIANGLES)                # 開始繪製三角形（z 軸正半區）

        glColor4f(1.0, 0.0, 0.0, 1.0)        # 設置當前顏色爲紅色不透明
        glVertex3f(-0.5, 0.5, 0.5)           # 設置三角形頂點
        glColor4f(0.0, 1.0, 0.0, 1.0)        # 設置當前顏色爲綠色不透明
        glVertex3f(0.5, 0.5, 0.5)            # 設置三角形頂點
        glColor4f(0.0, 0.0, 1.0, 1.0)        # 設置當前顏色爲藍色不透明
        glVertex3f(0.0, -0.366, 0.5)         # 設置三角形頂點

        glEnd()                              # 結束繪製三角形
