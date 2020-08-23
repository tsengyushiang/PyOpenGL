def save_withTexture(filename, sampleTexture, matName):
    mtlF = open(filename, "w")
    mtlF.write('newmtl '+matName+'\n')
    mtlF.write('Ns 96.078431\n')
    mtlF.write('Ka 0.000000 0.000000 0.000000\n')
    mtlF.write('Kd 1.000000 1.000000 1.000000\n')
    mtlF.write('Ks 0.000000 0.000000 0.000000\n')
    mtlF.write('Ni 1.000000\n')
    mtlF.write('d 1.000000\n')
    mtlF.write('illum 2\n')
    mtlF.write('map_Kd '+sampleTexture+'\n')

    mtlF.close()
