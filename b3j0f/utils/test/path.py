#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase, main

from b3j0f.utils.path import lookup, getpath


def _test():
    pass


class UtilsTest(TestCase):

    def setUp(self):
        pass

    def test_lookup(self):

        # resolve builtin function
        _open = lookup('%s.open' % open.__module__)

        self.assertTrue(_open is open)

        # resolve class
        utilsTest = lookup('b3j0f.utils.test.path.UtilsTest')

        self.assertTrue(utilsTest is UtilsTest)

        # do not resolve method
        setUp = lookup('b3j0f.utils.test.path.UtilsTest.setUp')

        self.assertFalse(setUp is UtilsTest.setUp)

        # resolve function
        test = lookup('b3j0f.utils.test.path._test')

        self.assertTrue(_test is test)

        # resolve resolve_element
        _resolve_element = lookup(
            'b3j0f.utils.path.lookup')

        self.assertTrue(_resolve_element is lookup)

        # resolve package and sub-module
        b3j0f = lookup('b3j0f')

        self.assertTrue(b3j0f is not None)
        self.assertEqual(b3j0f.__name__, 'b3j0f')

        b3j0f_utils = lookup('b3j0f.utils')

        self.assertTrue(b3j0f_utils is not None)
        self.assertTrue(b3j0f_utils is not b3j0f)
        self.assertEqual(b3j0f_utils.__name__, 'b3j0f.utils')

        # resolve local variables
        a = 1
        _a = lookup('a')
        self.assertTrue(_a is a)

        # resolve global variables
        self.assertTrue(lookup('UtilsTest') is UtilsTest)

    def test_getpath(self):

        # resolve built-in function
        open_path = getpath(open)

        self.assertEqual(open_path, '%s.open' % open.__module__)

        # resolve global class
        self.assertEqual(
            getpath(UtilsTest), 'b3j0f.utils.test.path.UtilsTest')

        # resolve reciproque with resolve
        self.assertEqual(lookup(getpath(open)), open)

if __name__ == '__main__':
    main()
