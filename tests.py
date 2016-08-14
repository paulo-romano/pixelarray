from unittest import TestCase
from pixelarray import PixelArray


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

    def _get_pixelarray_and_expected(self):
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
