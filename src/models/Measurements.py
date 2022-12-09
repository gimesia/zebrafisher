class Measurements:

    def __init__(self):
        self.resolution: float = None
        self.eye_count: 1 | 2 | 0 = 0
        self.eye1_diameter_major: float = None
        self.eye2_diameter_major: float = None
        self.axis_major: float = None
        self.axis_minor: float = None
        self.axes_ratio: float = None
        self.area: float = None
        self.times = [0,0,0,0]

    def calculate_resolution(self, r: int) -> float:
        """
        Calculates resolution from well radius

        :param r: radius in pixels
        :return:  resolution in mm/pixel
        """
        self.resolution = 7.0 / (r * 2.0)
        return self.resolution

    def calculate_axes_ratio(self) -> float:
        """
        Calculates & stores ratio of measured axes

        :return: ratio of axes
        """
        if not self.axis_minor or not self.axis_major:
            raise Exception("Missing axes!")
        self.axes_ratio = self.axis_major / self.axis_minor
        return self.axes_ratio
