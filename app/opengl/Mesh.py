
class Mesh():
    def __init__(self, mat, geo):
        self.material = mat
        self.geometry = geo

    def draw(self):
        self.material.activate()
        self.geometry.draw()
        self.material.deactivate()
