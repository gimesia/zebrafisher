from datetime import datetime, timedelta


class Timer:
    def __init__(self):
        self.start: datetime = datetime.now()
        self.end: datetime = None
        self.duration: timedelta = None

    def stop(self):
        self.end = datetime.now()
        self.duration = self.end - self.start


if __name__ == '__main__':
    t = Timer()
