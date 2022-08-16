import cv2
import numpy as np


def msg(title: str, data: any = None):
    print(f"# {title}")
    if data:
        print(f"{data}\n")
    print("_____________________________________________________________")


def show_img(image: np.ndarray, title="Image"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_multiple_img(images: list[np.ndarray]):
    index = 0

    for i in images:
        cv2.imshow(str(index), i)
        index += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()

