#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main

from b3j0f.utils.ut import UTCase
from b3j0f.utils.reflect import base_elts


class BaseEltsTest(UTCase):
    """
    Test base_elts function
    """

    def test_not_inherited(self):
        """
        Test with a not inherited element.
        """

        bases = base_elts(None)
        self.assertFalse(bases)

    def test_function(self):
        """
        Test function
        """

        bases = base_elts(lambda: None)
        self.assertFalse(bases)

    def test_class(self):
        """
        Test class
        """

        class A:
            pass

        class B(A, dict):
            pass

        bases = base_elts(B)
        self.assertEqual(bases, set(B.__bases__))

    def test_method(self):
        """
        Test method
        """

        class A:
            def a(self):
                pass

        class B(A):
            pass

        bases = base_elts(B.a, cls=B)
        self.assertEqual(len(bases), 1)
        base = bases.pop()
        self.assertEqual(base, A.a)

    def test_not_method(self):
        """
        Test when method has been overriden
        """

        class A:
            def a(self):
                pass

        class B(A):
            def a(self):
                pass

        bases = base_elts(B.a, cls=B)
        self.assertFalse(bases)

    def test_boundmethod(self):
        """
        Test bound method
        """

        class Test:
            def test(self):
                pass

        test = Test()

        bases = base_elts(test.test)
        self.assertEqual(len(bases), 1)
        self.assertEqual(bases.pop(), Test.test)

    def test_not_boundmethod(self):
        """
        Test with a bound method which is only defined in the instance
        """

        class Test:
            def test(self):
                pass

        test = Test()
        test.test = lambda self: None

        bases = base_elts(test.test)
        self.assertFalse(bases)


if __name__ == '__main__':
    main()
