class PixelArray:
    """Implements a array of pixels"""
    def __init__(self, number_of_cols, number_of_rows):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self._initialize_data(number_of_cols, number_of_rows)

    def __len__(self):
        return self.number_of_rows * self.number_of_cols

    def _initialize_data(self, number_of_cols, number_of_rows):
        self._data = []
        for row in range(number_of_rows):
            self._data.append(list(['0' for col in range(number_of_cols)]))

    def clear(self):
        self._initialize_data(self.number_of_cols, self.number_of_rows)

    @property
    def data(self):
        return self._data

    def _verify_coordinates(self, x, y):
        if not x:
            raise ValueError('X must be a non zero value')
        if not y:
            raise ValueError('y must be a non zero value')

    def get_pixel(self, x, y):
        self._verify_coordinates(x, y)
        return self._data[y-1][x-1]

    def colorize(self, x, y, color):
        self._verify_coordinates(x, y)
        self._data[y-1][x-1] = color

    def get_formated_data(self):
        formated_data = ''
        for row in self.data:
            for col in row:
                formated_data += col
            formated_data += '\n'

        return formated_data
