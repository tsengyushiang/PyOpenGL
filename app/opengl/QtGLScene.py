from PyQt5.QtWidgets import QOpenGLWidget


class QtGLScene(QOpenGLWidget):
    def __init__(self, version_profile=None, parent=None):
        super(QtGLScene, self).__init__(parent)
        self.version_profile = version_profile

    def initializeGL(self):
        self.gl = self.context().versionFunctions(self.version_profile)
        self.gl.initializeGLFunctions()

        self.gl.glClearColor(1.0, 0.5, 0.5, 1.0)
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)

    def paintGL(self):
        prnit('drawing')

    def resizeGL(self, width, height):
        pass
