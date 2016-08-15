from unittest import TestCase
from unittest.mock import MagicMock
from pixelarray import PixelArray, Runner


class PixelArrayTestCase(TestCase):
    def test_must_have_pixelarray_class(self):
        self.assertIsNotNone(PixelArray)

    def test_must_initialize_with_size(self):
        self.assertIsNotNone(PixelArray(5, 5))

    def test_must_implement_dunder_len(self):
        obj = PixelArray(5, 5)
        self.assertEqual(len(obj), 25)

    def test_data_property_must_be_mxn_array(self):
        m, n = 5, 10
        obj = PixelArray(m, n)

        # assert count rows
        self.assertEqual(len(obj.data), n)

        # assert count cols
        for row in obj.data:
            with self.subTest():
                self.assertEqual(len(row), m)

    def test_initial_elements_must_have_zero_value(self):
        obj = PixelArray(3, 2)

        for rows in obj.data:
            for col in rows:
                with self.subTest():
                    self.assertEqual(col, '0')

    def test_get_pixel_must_return_x_y_value(self):
        obj = PixelArray(5, 5)
        x, y, new_value = 2, 3, 'w'
        obj.data[y-1][x-1] = new_value
        self.assertEqual(obj.get_pixel(x, y), new_value)

    def assertValidCoordinates(self, callable_obj, **kwargs):
        self.assertRaises(ValueError, callable_obj, x=0, y=1, **kwargs)
        self.assertRaises(ValueError, callable_obj, x=1, y=0, **kwargs)

    def test_get_pixel_coordinates_must_be_non_zero(self):
        obj = PixelArray(5, 5)
        self.assertValidCoordinates(obj.get_pixel)

    def test_colorize_method_must_change_element_value(self):
        obj = PixelArray(5, 5)
        x, y, new_value = 2, 3, 'w'
        obj.colorize(x, y, new_value)
        self.assertEqual(obj.get_pixel(x, y), new_value)

    def test_colorize_coordinates_must_be_non_zero(self):
        obj = PixelArray(5, 5)
        self.assertValidCoordinates(obj.colorize, color='d')

    def test_get_formatted_data(self):
        expected = 'F0F00\n' \
                   '00000\n' \
                   '0A000\n' \
                   '00000\n' \
                   '00000\n' \
                   '0000A\n'

        obj = PixelArray(5, 6)
        obj.colorize(1, 1, 'F')
        obj.colorize(3, 1, 'F')
        obj.colorize(2, 3, 'A')
        obj.colorize(5, 6, 'A')
        self.assertEqual(obj.get_formatted_data(), expected)

    def test_clear_method_must_reinitialize_data(self):
        expected = '00000\n' \
                   '00000\n' \
                   '00000\n' \
                   '00000\n' \
                   '00000\n' \
                   '00000\n'

        obj = PixelArray(5, 6)
        obj.colorize(1, 1, 'F')
        obj.colorize(3, 1, 'F')
        obj.colorize(2, 3, 'A')
        obj.colorize(5, 6, 'A')
        obj.clear()
        self.assertEqual(obj.get_formatted_data(), expected)

    def test_draw_vertical_segment_method(self):
        expected = '10000\n' \
                   '10E00\n' \
                   '10E0X\n' \
                   '1000X\n'

        obj = PixelArray(5, 4)
        obj.draw_vertical_segment(3, 2, 3, 'E')
        obj.draw_vertical_segment(5, 3, 4, 'X')
        obj.draw_vertical_segment(1, 1, 4, '1')
        self.assertEqual(obj.get_formatted_data(), expected)

    def test_draw_horizontal_segment_method(self):
        expected = '00000\n' \
                   'XXXXX\n' \
                   'EEE00\n' \
                   '000YY\n'

        obj = PixelArray(5, 4)
        obj.draw_horizontal_segment(1, 5, 2, 'X')
        obj.draw_horizontal_segment(1, 3, 3, 'E')
        obj.draw_horizontal_segment(4, 5, 4, 'Y')
        self.assertEqual(obj.get_formatted_data(), expected)

    def test_draw_rectangle_method(self):
        expected = 'XXXX000000\n' \
                   'XXXX000000\n' \
                   'RR00000000\n' \
                   'RR00000000\n' \
                   'RR00000000\n' \
                   'RR00000000\n' \
                   '0EEEEEEE00\n' \
                   '0EEEEEEE00\n' \
                   '0000000000\n'

        obj = PixelArray(10, 9)
        obj.draw_rectangle(1, 1, 4, 2, 'X')
        obj.draw_rectangle(2, 7, 8, 8, 'E')
        obj.draw_rectangle(1, 3, 2, 6, 'R')
        self.assertEqual(obj.get_formatted_data(), expected)

    def test_verify_coordinates_method(self):
        obj = PixelArray(2, 2)
        self.assertRaises(ValueError, obj._verify_coordinates, x=0, y=1)
        self.assertRaises(ValueError, obj._verify_coordinates, x=1, y=0)
        self.assertRaises(ValueError, obj._verify_coordinates, x=-1, y=1)
        self.assertRaises(ValueError, obj._verify_coordinates, x=1, y=-1)
        self.assertRaises(ValueError, obj._verify_coordinates, x=3, y=1)
        self.assertRaises(ValueError, obj._verify_coordinates, x=1, y=3)

    def test_verify_coordinates_return_false(self):
        obj = PixelArray(2, 2)
        self.assertFalse(obj._verify_coordinates(-1, 2, throw_exception=False))
        self.assertFalse(obj._verify_coordinates(1, -2, throw_exception=False))

    @staticmethod
    def _get_pixelarray_and_expected():
        expected = 'KKKK000000\n' \
                   'KKKK000000\n' \
                   'RR00000000\n' \
                   'RR00000000\n' \
                   'RR00000000\n' \
                   'RR00000000\n' \
                   '0JJJJJJJ00\n' \
                   '0JJJJJJJ00\n' \
                   '0000000000\n'

        obj = PixelArray(10, 9)
        obj.draw_rectangle(1, 1, 4, 2, 'X')
        obj.draw_rectangle(2, 7, 8, 8, 'E')
        obj.draw_rectangle(1, 3, 2, 6, 'R')
        obj.fill_region(2, 2, 'K')
        obj.fill_region(3, 8, 'J')

        return expected, obj

    def test_fill_region_method(self):
        expected, obj = self._get_pixelarray_and_expected()
        self.assertEqual(obj.get_formatted_data(), expected)

    def test_must_save_formatted_data_to_file(self):
        import os
        expected, obj = self._get_pixelarray_and_expected()
        name = 'test.bmp'
        obj.save(name)
        file = open(name).read()
        os.remove(name)
        self.assertEqual(file, expected)

    def test_recursion_limit(self):
        max_number = 10
        obj = PixelArray(max_number, max_number)
        obj.fill_region(1, 1, 'X')
        self.assertIsNotNone(obj)


class RunnerTestCase(TestCase):
    def setUp(self):
        self.runner = Runner()

    def test_must_have_run_method(self):
        self.assertIsNotNone(self.runner.run)

    def test_must_have_execute_method(self):
        self.assertIsNotNone(self.runner.execute)

    def assertExecute(self, command, command_args):
        method_name = 'execute_' + command

        # Mock the method
        method_old = getattr(self.runner, method_name)
        setattr(self.runner, method_name, MagicMock())
        self.runner.execute(command, command_args)

        # Verify if the method was called
        getattr(self.runner, method_name).assert_called_with(command_args)

        # Change mocked method to old one
        setattr(self.runner, method_name, method_old)

    def test_execute_must_execute_i(self):
        command, command_args = 'i', ['4', '2']
        self.assertExecute(command, command_args)

    def test_execute_must_execute_c(self):
        command, command_args = 'c', None
        self.assertExecute(command, command_args)

    def test_execute_must_execute_l(self):
        command, command_args = 'l', ['2', '3', 'C']
        self.assertExecute(command, command_args)

    def test_execute_must_execute_v(self):
        command, command_args = 'v', ['3', '3', '6', 'C']
        self.assertExecute(command, command_args)

    def test_execute_must_execute_h(self):
        command, command_args = 'h', ['6', '5', '6', 'C']
        self.assertExecute(command, command_args)

    def test_execute_must_execute_k(self):
        command, command_args = 'k', ['3', '6', '5', '6', 'C']
        self.assertExecute(command, command_args)

    def test_execute_must_execute_f(self):
        command, command_args = 'f', ['3', '6', 'C']
        self.assertExecute(command, command_args)

    def test_execute_must_execute_s(self):
        command, command_args = 's', ['test.bmp']
        self.assertExecute(command, command_args)

    def assertExecuteErrorMessage(self, command_method, command_args, error_message):
        # Mock the method
        method_old = self.runner._print_error
        self.runner._print_error = MagicMock()
        command_method(command_args)

        # Verify if the method was called
        self.runner._print_error.assert_called_with(error_message)

        # Change mocked method to old one
        self.runner._print_error = method_old

    def test_execute_i_must_print_error_message_if_command_format_error(self):
        self.assertExecuteErrorMessage(self.runner.execute_i, ['10'],
                                       'Invalid command! Must be: i number_of_columns number_of_rows')

    def test_execute_c_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_c, [],
                                       'Invalid command! Must be initialized first.')

    def test_execute_l_must_print_error_message_if_command_format_error(self):
        self.runner.execute_i(['2', '2'])
        self.assertExecuteErrorMessage(self.runner.execute_l, [],
                                       'Invalid command! Must be: L Pos_X Pos_Y Color')

    def test_execute_l_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_l, ['2', '2', 'C'],
                                       'Invalid command! Must be initialized first.')

    def test_execute_v_must_print_error_message_if_command_format_error(self):
        self.runner.execute_i(['2', '2'])
        self.assertExecuteErrorMessage(self.runner.execute_v, [],
                                       'Invalid command! Must be: V Pos_X Pos_Y1 Pos_Y2 Color')

    def test_execute_v_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_v, ['1', '1', '1', 'C'],
                                       'Invalid command! Must be initialized first.')

    def test_execute_h_must_print_error_message_if_command_format_error(self):
        self.runner.execute_i(['2', '2'])
        self.assertExecuteErrorMessage(self.runner.execute_h, [],
                                       'Invalid command! Must be: H Pos_X1 Pos_X2 Pos_Y Color')

    def test_execute_h_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_h, ['1', '1', '1', 'C'],
                                       'Invalid command! Must be initialized first.')

    def test_execute_k_must_print_error_message_if_command_format_error(self):
        self.runner.execute_i(['2', '2'])
        self.assertExecuteErrorMessage(self.runner.execute_k, [],
                                       'Invalid command! Must be: K Pos_X1 Pos_Y1 Pos_X2 Pos_Y2 Color')

    def test_execute_k_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_k, ['1', '1', '1', '1', 'C'],
                                       'Invalid command! Must be initialized first.')

    def test_execute_f_must_print_error_message_if_command_format_error(self):
        self.runner.execute_i(['2', '2'])
        self.assertExecuteErrorMessage(self.runner.execute_f, [],
                                       'Invalid command! Must be: f Pos_X Pos_Y Color')

    def test_execute_f_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_f, ['1', '1', '1', '1', 'C'],
                                       'Invalid command! Must be initialized first.')

    def test_execute_s_must_print_error_message_if_command_format_error(self):
        self.runner.execute_i(['2', '2'])
        self.assertExecuteErrorMessage(self.runner.execute_s, [],
                                       'Invalid command! Must be: S Name')

    def test_execute_s_must_print_error_message_if_not_initialized(self):
        self.assertExecuteErrorMessage(self.runner.execute_s, ['1', '1', '1', '1', 'C'],
                                       'Invalid command! Must be initialized first.')


class ExerciseTestcase(TestCase):
    def setUp(self):
        self.runner = Runner()

    def assertFileEqual(self, file_name, expected):
        import os
        file = open(file_name).read()
        os.remove(file_name)
        self.assertEqual(file, expected)

    def test_one(self):
        file_name = 'one.bmp'
        expected = '00000\n' \
                   '00000\n' \
                   '0A000\n' \
                   '00000\n' \
                   '00000\n' \
                   '00000\n'

        self.runner.execute('i', ['5', '6'])
        self.runner.execute('l', ['2', '3', 'A'])
        self.runner.execute('s', [file_name])

        self.assertFileEqual(file_name, expected)

    def test_two(self):
        file_name = 'two.bmp'
        expected = 'JJJJJ\n' \
                   'JJZZJ\n' \
                   'JWJJJ\n' \
                   'JWJJJ\n' \
                   'JJJJJ\n' \
                   'JJJJJ\n'

        self.runner.execute('i', ['5', '6'])
        self.runner.execute('g', ['2', '3', 'J'])
        self.runner.execute('v', ['2', '3', '4', 'W'])
        self.runner.execute('h', ['3', '4', '2', 'Z'])
        self.runner.execute('f', ['3', '3', 'J'])
        self.runner.execute('s', [file_name])

        self.assertFileEqual(file_name, expected)

    def test_three(self):
        file_name = 'three.bmp'
        expected = 'JJJJJJJJJJ\n' \
                   'JJJJJJJJJJ\n' \
                   'JWJJAJJJJJ\n' \
                   'JWJJJJJJJJ\n' \
                   'ZZZZZZZZZZ\n' \
                   'RRRRRRRRRR\n' \
                   'REEEEEEERR\n' \
                   'REEEEEEERR\n' \
                   'RRRRRRRRRR\n'

        self.runner.execute('i', ['10', '9'])
        self.runner.execute('l', ['5', '3', 'A'])
        self.runner.execute('g', ['2', '3', 'J'])
        self.runner.execute('v', ['2', '3', '4', 'W'])
        self.runner.execute('h', ['1', '10', '5', 'Z'])
        self.runner.execute('f', ['3', '3', 'J'])
        self.runner.execute('k', ['2', '7', '8', '8', 'E'])
        self.runner.execute('f', ['9', '9', 'R'])
        self.runner.execute('s', [file_name])

        self.assertFileEqual(file_name, expected)
