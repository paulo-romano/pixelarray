class PixelArray:
    """Implements a array of pixels"""
    def __init__(self, m, n):
        self.m = m
        self.n = n

    def __len__(self):
        return self.m * self.n
