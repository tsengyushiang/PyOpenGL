from opengl.GlutScene import *
from opengl.Geometry import *
from opengl.Texture import *
from opengl.ShaderMaterial import *
from opengl.Mesh import *

import shaders.texture2D as myShader

from Args.singleModelAndTexture import build_argparser
args = build_argparser().parse_args()

window = GlutScene()

# read shader
mat = ShaderMaterial(myShader.vertex_shader,
                     myShader.fragment_shader)

# read obj file
geo = Geometry(args.model)


mesh = Mesh(mat, geo)

# read texture
texture = Texture(args.texture)

window.add(mesh)
window.MainLoop()
