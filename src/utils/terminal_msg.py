import cv2
import numpy as np


def msg(title: str, data: any = None):
    """
    Prints blocked text on the console
    :param title: string to be written
    :param data: data to be displayed
    """
    print(f"# {title}")
    if data:
        print(f"{data}\n")
    print("_____________________________________________________________")


def show_img(image: np.ndarray, title="Image"):
    """
    Opens image in a popup window

    :param image: image to be displayed
    :param title: title of the popup window
    """
    if image.dtype == 'bool':
        image = image.astype(float)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_multiple_img(images: list[np.ndarray]):
    """
    Performs show_img() function on list of images

    :param images: list of images to be displayed
    """
    index = 0

    for i in images:
        cv2.imshow(str(index), i)
        index += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()
