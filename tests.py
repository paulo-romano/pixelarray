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

    def test_must_have_get_data_function(self):
        obj = PixelArray(5, 5)
        self.assertIsNotNone(obj.get_data)

    def test_get_data_must_return_mxn_array(self):
        m, n = 5, 10
        obj = PixelArray(m, n)
        data = obj.get_data()

        self.assertEqual(len(data), m)
        for row in data:
            with self.subTest():
                self.assertEqual(len(row), n)

