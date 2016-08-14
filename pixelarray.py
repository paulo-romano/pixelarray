class PixelArray:
    """Implements a array of pixels"""
    def __init__(self, number_of_cols, number_of_rows):
        """
        Initializer a PixelArray object
        :param number_of_cols: Number of columns
        :param number_of_rows: Number of rows
        """
        self.number_of_rows = number_of_rows
        self.number_of_cols = number_of_cols
        self._initialize_data(number_of_cols, number_of_rows)

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
        :param x: Column of the pixel
        :param y: Line of the pixel
        :param region_color: The region color that will be verified
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
        """
        Fill region with new color
        :param x: Column of the pixel in region
        :param y: Line of the pixel in region
        :param color: New color
        """
        region_color = self.get_pixel(x, y)
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
    def __init__(self):
        self._data = None

    def execute_i(self, args):
        """
        Create a empty array of pixels
        :param args: Args used in this command
        """
        try:
            cols = int(args[0])
            rows = int(args[1])
            self._data = PixelArray(cols, rows)
        except:
            print('Invalid command! Must be: i number_of_columns number_of_rows')

    def execute_c(self, command_args):
        """
        Clear the data
        :param command_args: Args used in this command
        """
        try:
            self._data.clear()
        except AttributeError:
            print('Inválide command! Must be initialized first.')

    def execute_l(self, args):
        """
        Coloraze a pixel
        :param args: Args used in this command
        """
        try:
            x = int(args[0])
            y = int(args[1])
            color = str(args[2])
            self._data.colorize(x, y, color)
        except AttributeError:
            print('Inválide command! Must be initialized first.')
        except:
            print('Invalid command! Must be: L Pos_X Pos_Y Color')

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
            print('Inválide command! Must be initialized first.')
        except:
            print('Invalid command! Must be: V Pos_X Pos_Y1 Pos_Y2 Color')

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
            print('Inválide command! Must be initialized first.')
        except:
            print('Invalid command! Must be: H Pos_X1 Pos_X2 Pos_Y Color')

    def execute_k(self, args):
        """
        Draw a rectangle
        :param args: Args used in this command
        """
        try:
            x1 = int(args[0])
            x2 = int(args[1])
            y1 = int(args[2])
            y2 = int(args[3])
            color = str(args[4])
            self._data.draw_rectangle(x1, y1, x2, y2, color)
        except AttributeError:
            print('Inválide command! Must be initialized first.')
        except:
            print('Invalid command! Must be: K Pos_X1 Pos_Y1 Pos_X2 Pos_Y2 Color')

    def execute_f(self, args):
        """
        Coloraze a region
        :param args: Args used in this command
        """
        try:
            x = int(args[0])
            y = int(args[1])
            color = str(args[2])
            self._data.colorize(x, y, color)
        except AttributeError:
            print('Inválide command! Must be initialized first.')
        except:
            print('Invalid command! Must be: f Pos_X Pos_Y Color')

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


