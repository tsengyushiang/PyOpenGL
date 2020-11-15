import cv2


input = 'C:/Users/tseng/Downloads/lapras/20200925140117394107.932122061823.color.png'
output = 'C:/Users/tseng/Downloads/lapras/20200925140117394107_932122061823.png'

img = cv2.imread(input)
mask = cv2.imread(output,0)
resize_mask = cv2.resize(mask, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)

res = cv2.bitwise_and(img,img,mask = resize_mask)

cv2.imwrite(input,res)