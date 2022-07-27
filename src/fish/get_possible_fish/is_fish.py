from skimage.measure import regionprops


def is_fish(labeled_data) -> [bool, object]:
    """
    Decides whether a label object is a fish, returns the properties
    :param

    """

    reg_props = regionprops(labeled_data)

    if reg_props[0].eccentricity < 0.9:  # 0.92
        fish = True
    else:
        fish = False

    props: object

    props.area = reg_props[0].area
    props.obj_height = reg_props[0].bbox[3] - reg_props[0].bbox[1]  # y2-y1
    props.obj_width = reg_props[0].bbox[2] - reg_props[0].bbox[0]  # x2-x1

    return fish, props
