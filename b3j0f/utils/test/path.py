#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase, main

from b3j0f.utils.path import resolve_path, get_path


def _test():
    pass


class UtilsTest(TestCase):

    def setUp(self):
        pass

    def test_resolve_element(self):

        # resolve builtin function
        _open = resolve_path('__builtin__.open')

        self.assertTrue(_open is open)

        # resolve class
        utilsTest = resolve_path('b3j0f.utils.test.path.UtilsTest')

        self.assertTrue(utilsTest is UtilsTest)

        # do not resolve method
        setUp = resolve_path('b3j0f.utils.test.path.UtilsTest.setUp')

        self.assertFalse(setUp is UtilsTest.setUp)

        # resolve function
        test = resolve_path('b3j0f.utils.test.path._test')

        self.assertTrue(_test is test)

        # resolve resolve element
        _resolve_element = resolve_path(
            'b3j0f.utils.path.resolve_path')

        self.assertTrue(_resolve_element is resolve_path)

    def test_path(self):

        open_path = get_path(open)

        self.assertEqual(open_path, '__builtin__.open')

        self.assertEqual(
            get_path(UtilsTest), 'b3j0f.utils.test.path.UtilsTest')

        self.assertEqual(resolve_path(get_path(open)), open)

if __name__ == '__main__':
    main()
