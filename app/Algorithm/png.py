def removeBorder(image, kernel_size=3):
    img_RGBA = image.copy()
    height, width, channels = image.shape

    for x in range(kernel_size, width-kernel_size):
        for y in range(kernel_size, height-kernel_size):

            if(image[y, x][3] != 0):

                isBorderPixel = False
                for i in range(-kernel_size, kernel_size):
                    for j in range(-kernel_size, kernel_size):
                        if(image[y+j, x+i][3] == 0):
                            isBorderPixel = True
                            break

                    if(isBorderPixel):
                        break

                if(isBorderPixel):
                    img_RGBA[y, x] = [0, 0, 0, 0]

    return img_RGBA


def addBorder(image, kernel_size=7):
    img_RGBA = image.copy()
    height, width, channels = image.shape

    for x in range(kernel_size, width-kernel_size):
        for y in range(kernel_size, height-kernel_size):

            if(image[y, x][3] == 0):

                v = [0.0, 0.0]
                count = 0.0
                for i in range(-kernel_size, kernel_size):
                    for j in range(-kernel_size, kernel_size):
                        if(image[y+j, x+i][3] != 0):
                            v[0] += float(j)
                            v[1] += float(i)
                            count += 1.0

                if(count != 0.0):
                    v[0] /= count
                    v[1] /= count
                    img_RGBA[y, x] = image[int(y+v[0]), int(x+v[1])]
                    img_RGBA[y, x][3] = 255
    return img_RGBA


def tuneBorder(image):
    imgRemoveBorder = removeBorder(image,3)
    imgAddBorder= addBorder(imgRemoveBorder,7)
    return imgAddBorder