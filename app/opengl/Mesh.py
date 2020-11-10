
class Mesh():
    def __init__(self, mat, geo):
        self.material = mat
        self.geometry = geo
        self.visible=True

    def init(self):
        shader = self.material.init()
        self.geometry.shader = shader
        self.geometry.init()

    def draw(self):
        self.material.activate()
        if self.visible:
            self.geometry.draw()
        self.material.deactivate()
