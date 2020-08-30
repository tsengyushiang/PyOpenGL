def Load(objPath):

    objfile = open(objPath, 'r')
    Lines = objfile.readlines()

    vertices = []
    normals = []
    faces = []

    # Strips the newline character
    for line in Lines:
        contents = line.split()

        if contents[0] == 'v':
            vertices.append([float(contents[1]), float(
                contents[2]), float(contents[3])])
            normals.append([float(contents[4]), float(
                contents[5]), float(contents[6])])

        elif contents[0] == 'f':
            faces.append([float(contents[1]), float(
                contents[2]), float(contents[3])])

    return vertices, normals, faces


def save(objPath, mtlPath, Material, vertices, uvs, normals, faces):

    outF = open(objPath, "w")

    outF.write('mtllib '+mtlPath+'\n')
    outF.write('usemtl '+Material+'\n')
    outF.write('s off\n')

    for vertex in vertices:
        outF.write("v {0} {1} {2}\n".format(vertex[0], vertex[1], vertex[2]))

    for coord in uvs:
        outF.write("vt {0} {1}\n".format(coord[0], coord[1]))

    for n in normals:
        outF.write("vn {0} {1} {2}\n".format(n[0], n[1], n[2]))

    for f in faces:
        outF.write(
            "f {0}/{1} {2}/{3} {4}/{5}\n".format(
                int(f[0][0]), int(f[0][1]), int(f[1][0]), int(f[1][1]), int(f[2][0]), int(f[2][1])))

    outF.close()
