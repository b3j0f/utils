#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2015 Jonathan Labéjof <jonathan.labejof@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------

from unittest import main

from inspect import getargspec

from b3j0f.utils.ut import UTCase
from b3j0f.utils.proxy import get_proxy


class GetProxyTest(UTCase):
    """Test get_proxy function.
    """

    def _assert_function(self, func):
        """Test to proxify a function.
        """

        func_argspec = getargspec(func)

        proxy = get_proxy(func)

        proxy_argspec = getargspec(proxy)

        self.assertEqual(proxy.__name__, func.__name__)
        self.assertEqual(proxy.__module__, func.__module__)
        self.assertEqual(proxy.__doc__, func.__doc__)

    def test_function_empty(self):

        def test():
            """Default test function.
            """
            pass

        self._assert_function(test)

    def test_instance(self):
        """Test to proxify an instance.
        """

    def test_class(self):
        """Test to proxify a class.
        """

    def test_method(self):
        """Test to proxify a method.
        """

if __name__ == 'main':
    main()
