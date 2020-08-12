

filename = './results/pifuhd_final/recon/result_test_512.obj'

# Using readlines()
objfile = open(filename, 'r')
Lines = objfile.readlines()

vertice = []
uv = []
normal = []
face = []

# Strips the newline character
for line in Lines:
    contents = line.split()

    if contents[0] == 'v':
        vertice.append([float(contents[1]), float(
            contents[2]), float(contents[3])])
        uv.append([float(contents[1])*0.5+0.5, float(contents[2])*0.5+0.5])
        normal.append([float(contents[4]), float(
            contents[5]), float(contents[6])])

    elif contents[0] == 'f':
        face.append([float(contents[1]), float(
            contents[2]), float(contents[3])])

outF = open("./sample.obj", "w")

outF.write('mtllib sample.mtl\n')
outF.write('usemtl Material\n')
outF.write('s off\n')

for vertex in vertice:
    outF.write("v {0} {1} {2}\n".format(vertex[0], vertex[1], vertex[2]))

for coord in uv:
    outF.write("vt {0} {1}\n".format(coord[0], coord[1]))

for n in normal:
    outF.write("vn {0} {1} {2}\n".format(n[0], n[1], n[2]))

for f in face:
    outF.write("f {0}/{0} {1}/{1} {2}/{2}\n".format(int(f[0]), int(f[1]), int(f[2])))

outF.close()

mtlF = open("./sample.mtl", "w")


mtlF.write('newmtl Material\n')
mtlF.write('Ns 96.078431\n')
mtlF.write('Ka 0.000000 0.000000 0.000000\n')
mtlF.write('Kd 0.000000 0.000000 0.000000\n')
mtlF.write('Ks 0.000000 0.000000 0.000000\n')
mtlF.write('Ni 1.000000\n')
mtlF.write('d 1.000000\n')
mtlF.write('illum 2\n')
mtlF.write('map_Kd test.png\n')


mtlF.close()
