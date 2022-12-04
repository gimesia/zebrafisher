class Measurements:

    def __init__(self):
        self.resolution: float = None
        self.head_to_tail_length: float = None
        self.eye_count: 1 | 2 | 0 = 0
        self.eye1_diameter_major: float = None
        self.eye2_diameter_major: float = None
        self.axis_major: float = None
        self.axis_minor: float = None
        self.axes_ratio: float = None
        self.area: float = None
        self.times = [0, 0, 0]

    def calculate_resolution(self, r: int) -> float:
        self.resolution = 7.0 / (r * 2.0)
        return self.resolution

    def calculate_axes_ratio(self):
        if self.axis_minor and self.axis_major:
            self.axes_ratio = self.axis_major / self.axis_minor
            return self.axes_ratio
        return
