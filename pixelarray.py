class PixelArray:
    """Implements a array of pixels"""
    def __init__(self, number_of_cols, number_of_rows):
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self._data = []
        for row in range(number_of_rows):
            self._data.append(list([0 for col in range(number_of_cols)]))

    def __len__(self):
        return self.number_of_rows * self.number_of_cols

    @property
    def data(self):
        return self._data

    def get_pixel(self, x, y):
        return self._data[x][y]

    def colorize(self, x, y, color):
        self._data[x][y] = color

    def get_formated_data(self):
        formated_data = ''
        for row in self.data:
            for col in row:
                formated_data += str(col)
            formated_data += '\n'

        return formated_data
