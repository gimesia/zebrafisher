"""
Homomorphic filter by: github.com/glasgio
https://github.com/glasgio/homomorphic-filter/blob/master/homofilt.py
"""

import numpy as np

# Homomorphic filter class
from src.InputImage import EXAMPLE_IMG
from src.terminal_msg import show_img


class HomomorphicFilter:
    """Homomorphic filter implemented with diferents filters and an option to an external filter.

    High-frequency filters implemented:
        butterworth
        gaussian
    Attributes:
        a, b: Floats used on emphasis filter:
            H = a + b*H

        .
    """

    def __init__(self, a=0.5, b=1.5):
        self.a = float(a)
        self.b = float(b)

    # Filters
    def __butterworth_filter(self, I_shape, filter_params):
        P = I_shape[0] / 2
        Q = I_shape[1] / 2
        U, V = np.meshgrid(range(I_shape[0]), range(I_shape[1]), sparse=False, indexing='ij')
        Duv = (((U - P) ** 2 + (V - Q) ** 2)).astype(float)
        H = 1 / (1 + (Duv / filter_params[0] ** 2) ** filter_params[1])
        return (1 - H)

    def __gaussian_filter(self, I_shape, filter_params):
        P = I_shape[0] / 2
        Q = I_shape[1] / 2
        H = np.zeros(I_shape)
        U, V = np.meshgrid(range(I_shape[0]), range(I_shape[1]), sparse=False, indexing='ij')
        Duv = (((U - P) ** 2 + (V - Q) ** 2)).astype(float)
        H = np.exp((-Duv / (2 * (filter_params[0]) ** 2)))
        return (1 - H)

    # Methods
    def __apply_filter(self, I, H):
        H = np.fft.fftshift(H)
        I_filtered = (self.a + self.b * H) * I
        return I_filtered

    def filter(self, I, filter_params, filter='butterworth', H=None):
        """
        Method to apply homormophic filter on an image
        Attributes:
            I: Single channel image
            filter_params: Parameters to be used on filters:
                butterworth:
                    filter_params[0]: Cutoff frequency
                    filter_params[1]: Order of filter
                gaussian:
                    filter_params[0]: Cutoff frequency
            filter: Choose of the filter, options:
                butterworth
                gaussian
                external
            H: Used to pass external filter
        """

        #  Validating image
        if len(I.shape) != 2:
            raise Exception('Improper image')

        # Take the image to log domain and then to frequency domain
        I_log = np.log1p(np.array(I, dtype="float"))
        I_fft = np.fft.fft2(I_log)

        # Filters
        if filter == 'butterworth':
            H = self.__butterworth_filter(I_shape=I_fft.shape, filter_params=filter_params)
        elif filter == 'gaussian':
            H = self.__gaussian_filter(I_shape=I_fft.shape, filter_params=filter_params)
        elif filter == 'external':
            print('external')
            if len(H.shape) != 2:
                raise Exception('Invalid external filter')
        else:
            raise Exception('Selected filter not implemented')

        # Apply filter on frequency domain then take the image back to spatial domain
        I_fft_filt = self.__apply_filter(I=I_fft, H=H)
        I_filt = np.fft.ifft2(I_fft_filt)
        I = np.exp(np.real(I_filt)) - 1
        return np.uint8(I)


# End of class HomomorphicFilter
import cv2 as cv


def homomorphic(img: np.ndarray, boost, cut_off, order, hndl):
    homomorphic_filter = HomomorphicFilter(a=0.85, b=3.0)
    return homomorphic_filter.filter(I=img, filter_params=[30, 2])

if __name__ == "__main__":
    import os

    image_path = r'/src/images/zf.jpg'
    directory = r'C:\Users\gimesia\Documents\PROJEKT\zebrafish_pipenv\src\images'
    filename = 'savedImage.jpg'

    # Main code
    print("Before saving image:")
    print(os.listdir(directory))

    img = EXAMPLE_IMG.processed
    img = cv.normalize(img, None, alpha=0, beta=255,
                       norm_type=cv.NORM_MINMAX)  # , alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    show_img(img)
    homo_filter = HomomorphicFilter(a=0.85, b=2.5)
    img_filtered = homo_filter.filter(I=img, filter_params=[30, 2])
    show_img(img_filtered)
    cv.imwrite(img=img_filtered, filename=filename)

    print("After saving image:")
    print(os.listdir(directory))

"""
homomorphic(image,boost,CutOff,order,hndl)
homomorphic(im, boost, CutOff, order, varargin)
"""
