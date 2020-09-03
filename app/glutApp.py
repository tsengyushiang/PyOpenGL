from opengl.Scene.GlutScene import *
from opengl.Geometry.ObjGeometry import *
from opengl.Material.ShaderMaterial import *
from opengl.Texture import *
from opengl.Mesh import *
from opengl.Uniform import *

import shaders.texture2D as myShader

from Args.singleModelAndTexture import build_argparser
args = build_argparser().parse_args()

window = GlutScene()

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
geo = ObjGeometry(args.model)

mesh = Mesh(mat, geo)

window.add(mesh)
window.MainLoop()
