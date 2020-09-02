
class Mesh():
    def __init__(self, mat, geo):
        self.material = mat
        self.geometry = geo

    def init(self):
        self.material.init()
        self.geometry.init()

    def draw(self):
        self.material.activate()
        self.geometry.draw()
        self.material.deactivate()
