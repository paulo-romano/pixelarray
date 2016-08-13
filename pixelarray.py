class PixelArray:
    """Implements a array of pixels"""
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self._data = []
        for row in range(m):
            self._data.append(list([0 for col in range(n)]))

    def __len__(self):
        return self.m * self.n

    def get_data(self):
        return self._data

    def get_pixel(self, x, y):
        return self._data[x][y]

    def colorize(self, x, y, color):
        self._data[x][y] = color
