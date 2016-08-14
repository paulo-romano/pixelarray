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

    def _verify_coordinates(self, x, y, throw_exception=True):
        if x <= 0 or x > self.number_of_cols:
            if throw_exception:
                raise ValueError('X must be a non zero value')
            else:
                return False
        if y <= 0 or y > self.number_of_rows:
            if throw_exception:
                raise ValueError('y must be a non zero value')
            else:
                return False

        return True

    def get_pixel(self, x, y):
        self._verify_coordinates(x, y)
        return self._data[y-1][x-1]

    def colorize(self, x, y, color):
        self._verify_coordinates(x, y)
        self._data[y-1][x-1] = color

    def get_formatted_data(self):
        formatted_data = ''
        for row in self.data:
            for col in row:
                formatted_data += col
            formatted_data += '\n'

        return formatted_data

    def draw_vertical_segment(self, x, y1, y2, color):
        for y in range(y1, y2+1):
            self.colorize(x, y, color)

    def draw_horizontal_segment(self, x1, x2, y, color):
        for x in range(x1, x2+1):
            self.colorize(x, y, color)

    def draw_rectangle(self, x1, y1, x2, y2, color):
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                self.colorize(x, y, color)

    def _can_fill_pixel(self, x, y, region_color):
        """
        Verify if a pixel can be filled with another color
        :param x: Column of the pixel
        :param y: Line of the pixel
        :param region_color: The region color that will be verifyed
        :return: True if can be changed
        """
        return self._verify_coordinates(x, y, False) and self.get_pixel(x, y) == region_color

    def _fill(self, x, y, region_color, color):
        """
        Fill all pixel located in same region color, and his adjacent pixels.
        :param x: Column of the pixel
        :param y: Line of the pixel
        :param region_color: The region color that will be verifyed
        :param color: New color
        """

        if self.get_pixel(x, y) == region_color:
            self.colorize(x, y, color)

        if self._can_fill_pixel(x, y - 1, region_color):
            self._fill(x, y - 1, region_color, color)

        if self._can_fill_pixel(x, y + 1, region_color):
            self._fill(x, y + 1, region_color, color)

        if self._can_fill_pixel(x + 1, y, region_color):
            self._fill(x + 1, y, region_color, color)

        if self._can_fill_pixel(x - 1, y, region_color):
            self._fill(x - 1, y, region_color, color)

    def fill_region(self, x, y, color):
        region_color = self.get_pixel(x, y)
        self._fill(x, y, region_color, color)
