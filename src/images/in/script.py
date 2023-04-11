
import numpy as np
import matplotlib.pyplot as plt
import czifile
import os
import cv2
import skimage


path = os.getcwd()
#print('Get current directory : ', path)
# print(ims)
path = "C:\\Users\\aron.gimesi\\Documents\\.codes\\zebrafisher\\src\\images\\in\\AB kontroll 3 nap"
ims = os.listdir(path)

for i, im in enumerate(ims):
    filename = path + f'\\{im}'
    if filename.split(sep='.')[-1] == 'czi':
        print(filename)

        tif = czifile.imread(filename)
        # print(tif)
        # print(tif.shape)
        gray = cv2.normalize(src=tif[0, :, :, 0], dst=None, alpha=0, beta=255,
                             norm_type=cv2.NORM_MINMAX).astype(np.uint8)
        # print(gray.shape)
        """        cv2.imshow(im, gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
        dst = f'{path}\\out\\{im}.jpg'
        print(dst)

        cv2.imwrite(dst, gray)
    else:
        print(f"{filename.split(sep='.')[-1]} file")
