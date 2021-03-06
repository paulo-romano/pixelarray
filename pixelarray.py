class PixelArray:
    """Implements a array of pixels"""
    def __init__(self, number_of_cols, number_of_rows, fill_strategy_recursive=False):
        """
        Initializer a PixelArray object
        :param number_of_cols: Number of columns
        :param number_of_rows: Number of rows
        :param fill_strategy_recursive: Strategy used to fill pixel area. True, will use recursive one.
        """
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self._initialize_data(number_of_cols, number_of_rows)
        self._fill_strategy_recursive = fill_strategy_recursive

    def __len__(self):
        return self.number_of_rows * self.number_of_cols

    def _initialize_data(self, number_of_cols, number_of_rows):
        """
        Initialize data with zeros
        :param number_of_cols: Number of columns
        :param number_of_rows: Number of rows
        """
        self._data = []
        for row in range(number_of_rows):
            self._data.append(list(['0' for col in range(number_of_cols)]))

    def clear(self):
        """Clear the data."""
        self._initialize_data(self.number_of_cols, self.number_of_rows)

    @property
    def data(self):
        return self._data

    def _verify_coordinates(self, x, y, throw_exception=True):
        """
        Verify if a coordinate is valid
        :param x:
        :param y:
        :param throw_exception: If True will raise a ValueError exception
        :return: True if valid position
        """
        error_message = None
        if x <= 0 or x > self.number_of_cols:
            error_message = 'X must be a valid position in array'
        if y <= 0 or y > self.number_of_rows:
            error_message = 'Y must be a valid position in array'

        if error_message:
            if throw_exception:
                raise ValueError(error_message)
            else:
                return False
        else:
            return True

    def get_pixel(self, x, y):
        """
        Return the pixel color
        :param x: Column of the pixel
        :param y: Line of the pixel
        :return: The pixel's color
        """
        self._verify_coordinates(x, y)
        return self._data[y-1][x-1]

    def colorize(self, x, y, color):
        """
        Change color of a pixel
        :param x: Column of the pixel
        :param y: Line of the pixel
        :param color: New color
        """
        self._verify_coordinates(x, y)
        self._data[y-1][x-1] = color

    def get_formatted_data(self):
        """Returns data with pretty format"""
        formatted_data = ''
        for row in self.data:
            for col in row:
                formatted_data += col
            formatted_data += '\n'

        return formatted_data

    def draw_vertical_segment(self, x, y1, y2, color):
        """
        Draw a vertical segment in column x from line y1 to y2
        :param x: In this column
        :param y1: From this line
        :param y2: To this line
        :param color: Whit this color
        """
        for y in range(y1, y2+1):
            self.colorize(x, y, color)

    def draw_horizontal_segment(self, x1, x2, y, color):
        """
        Draw a horizontal segment in line y from column x1 to x2
        :param x1: From this column
        :param x2: To this column
        :param y: In this line
        :param color: Whit this color
        """
        for x in range(x1, x2+1):
            self.colorize(x, y, color)

    def draw_rectangle(self, x1, y1, x2, y2, color):
        """
        Draw a rectangle from (x1, y2) to (x2, y2) pixel.
        :param x1: Column of the first pixel
        :param y1: Line of the first pixel
        :param x2: Column of the second pixel
        :param y2: Line of the second pixel
        :param color: Color to fill the rectangle
        """
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                self.colorize(x, y, color)

    def _can_fill_pixel(self, x, y, region_color):
        """
        Verify if a pixel can be filled with another color
        :param x: Column of the pixel
        :param y: Line of the pixel
        :param region_color: The region color that will be verified
        :return: True if can be changed
        """
        return self._verify_coordinates(x, y, False) and self.get_pixel(x, y) == region_color

    def _fill(self, x, y, region_color, color):
        """
        Fill all pixel located in same region color, and his adjacent pixels.
            Algorithm: FloodFill with iterative implementation.
                This implementation is slower than recursive one, but python tend to not work well with recursion

        :param x: Column of the pixel
        :param y: Line of the pixel
        :param region_color: The region color that will be verified
        :param color: New color
        """
        pixels_to_fill = set()
        if self._can_fill_pixel(x, y, region_color):
            pixels_to_fill.add((x, y))

        while pixels_to_fill:
            x, y = pixels_to_fill.pop()
            self.colorize(x, y, color)

            if self._can_fill_pixel(x - 1, y, region_color):
                pixels_to_fill.add((x - 1, y))
            if self._can_fill_pixel(x + 1, y, region_color):
                pixels_to_fill.add((x + 1, y))
            if self._can_fill_pixel(x, y - 1, region_color):
                pixels_to_fill.add((x, y - 1))
            if self._can_fill_pixel(x, y + 1, region_color):
                pixels_to_fill.add((x, y + 1))

    def _fill_recursive(self, x, y, region_color, color):
        """
        Fill all pixel located in same region color, and his adjacent pixels.
            Algorithm: FloodFill with recursive implementation
        :param x: Column of the pixel
        :param y: Line of the pixel
        :param region_color: The region color that will be verified
        :param color: New color
        """
        if self.get_pixel(x, y) == region_color:
            self.colorize(x, y, color)

        if self._can_fill_pixel(x, y - 1, region_color):
            self._fill_recursive(x, y - 1, region_color, color)

        if self._can_fill_pixel(x, y + 1, region_color):
            self._fill_recursive(x, y + 1, region_color, color)

        if self._can_fill_pixel(x + 1, y, region_color):
            self._fill_recursive(x + 1, y, region_color, color)

        if self._can_fill_pixel(x - 1, y, region_color):
            self._fill_recursive(x - 1, y, region_color, color)

    def fill_region(self, x, y, color):
        """
        Fill region with new color
        :param x: Column of the pixel in region
        :param y: Line of the pixel in region
        :param color: New color
        """
        import sys

        region_color = self.get_pixel(x, y)
        if self._fill_strategy_recursive:
            default_recursion_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(len(self) + 100)

            self._fill_recursive(x, y, region_color, color)

            sys.setrecursionlimit(default_recursion_limit)
        else:
            self._fill(x, y, region_color, color)

    def save(self, name):
        """
        Save formatted data to file
        :param name: Name of the file
        """
        file = open(name, 'w')
        file.write(self.get_formatted_data())
        file.close()


class Runner:
    def __init__(self, fill_strategy_recursive=False):
        """
        Initialize Runner object
        :param fill_strategy_recursive: Strategy used to fill pixel area. True, will use recursive one.
        """
        self._data = None
        self._fill_strategy_recursive = fill_strategy_recursive

    @staticmethod
    def _print_error(error_message):
        print(error_message)

    def execute_i(self, args):
        """
        Create a empty array of pixels
        :param args: Args used in this command
        """
        try:
            cols = int(args[0])
            rows = int(args[1])
            self._data = PixelArray(cols, rows, self._fill_strategy_recursive)
        except IndexError:
            self._print_error('Invalid command! Must be: i number_of_columns number_of_rows')

    def execute_c(self, args):
        """
        Clear the data
        :param args: Args used in this command
        """
        try:
            self._data.clear()
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')

    def execute_l(self, args):
        """
        Colorize a pixel
        :param args: Args used in this command
        """
        try:
            x = int(args[0])
            y = int(args[1])
            color = str(args[2])
            self._data.colorize(x, y, color)
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')
        except IndexError:
            self._print_error('Invalid command! Must be: L Pos_X Pos_Y Color')

    def execute_v(self, args):
        """
        Draw a vertical segment
        :param args: Args used in this command
        """
        try:
            x = int(args[0])
            y1 = int(args[1])
            y2 = int(args[2])
            color = str(args[3])
            self._data.draw_vertical_segment(x, y1, y2, color)
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')
        except IndexError:
            self._print_error('Invalid command! Must be: V Pos_X Pos_Y1 Pos_Y2 Color')

    def execute_h(self, args):
        """
        Draw a horizontal segment
        :param args: Args used in this command
        """
        try:
            x1 = int(args[0])
            x2 = int(args[1])
            y = int(args[2])
            color = str(args[3])
            self._data.draw_horizontal_segment(x1, x2, y, color)
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')
        except IndexError:
            self._print_error('Invalid command! Must be: H Pos_X1 Pos_X2 Pos_Y Color')

    def execute_k(self, args):
        """
        Draw a rectangle
        :param args: Args used in this command
        """
        try:
            x1 = int(args[0])
            y1 = int(args[1])
            x2 = int(args[2])
            y2 = int(args[3])
            color = str(args[4])
            self._data.draw_rectangle(x1, y1, x2, y2, color)
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')
        except IndexError:
            self._print_error('Invalid command! Must be: K Pos_X1 Pos_Y1 Pos_X2 Pos_Y2 Color')

    def execute_f(self, args):
        """
        Colorize a region
        :param args: Args used in this command
        """
        try:
            x = int(args[0])
            y = int(args[1])
            color = str(args[2])
            self._data.fill_region(x, y, color)
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')
        except IndexError:
            self._print_error('Invalid command! Must be: f Pos_X Pos_Y Color')

    def execute_s(self, args):
        """
        Save to file
        :param args: Args used in this command
        """
        try:
            name = str(args[0])
            self._data.save(name)
        except AttributeError:
            self._print_error('Invalid command! Must be initialized first.')
        except IndexError:
            self._print_error('Invalid command! Must be: S Name')

    def execute(self, command, command_args):
        """
        Decides what command will be executed
        :param command: Command letter
        :param command_args: Command Args
        """
        method = getattr(self, 'execute_' + command.lower(), None)
        if method:
            method(command_args)

    def run(self):
        """Read commands from user, until user press x key"""
        command = ''
        while command.upper() != 'X':
            command, *command_args = input('Command: ').split(' ')
            self.execute(command, command_args)


if __name__ == '__main__':
    Runner().run()


