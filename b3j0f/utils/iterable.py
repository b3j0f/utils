# -*- coding: utf-8 -*-

# --------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014 Jonathan Labéjof <jonathan.labejof@gmail.com>
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

"""Provides tools to manage iterable types."""

from __future__ import absolute_import

__all__ = ['isiterable', 'ensureiterable', 'first']

from sys import maxsize

from collections import Iterable


def isiterable(element, exclude=None):
    """Check whatever or not if input element is an iterable.

    :param element: element to check among iterable types.
    :param type/tuple exclude: not allowed types in the test.

    :Example:

    >>> isiterable({})
    True
    >>> isiterable({}, exclude=dict)
    False
    >>> isiterable({}, exclude=(dict,))
    False
    """

    # check for allowed type
    allowed = exclude is None or not isinstance(element, exclude)
    result = allowed and isinstance(element, Iterable)

    return result


def ensureiterable(value, iterable=list, exclude=None):
    """Convert a value into an iterable if it is not.

    :param object value: object to convert
    :param type iterable: iterable type to apply (default: list)
    :param type/tuple exclude: types to not convert

    :Example:

    >>> ensureiterable([])
    []
    >>> ensureiterable([], iterable=tuple)
    ()
    >>> ensureiterable('test', exclude=str)
    ['test']
    >>> ensureiterable('test')
    ['t', 'e', 's', 't']
    """

    result = value

    if not isiterable(value, exclude=exclude):
        result = [value]
        result = iterable(result)

    else:
        result = iterable(value)

    return result


def first(iterable, default=None):
    """Try to get input iterable first item or default if iterable is empty.

    :param Iterable iterable: iterable to iterate on.
    :param default: default value to get if input iterable is empty.
    :raises TypeError: if iterable is not an iterable value

    :Example:

    >>> first('tests')
    't'
    >>> first('', default='test')
    'test'
    >>> first([])
    None
    """

    result = default

    # start to get the iterable iterator (raises TypeError if iter)
    iterator = iter(iterable)
    # get first element
    try:
        result = next(iterator)
    except StopIteration: # if no element exist, result equals default
        pass

    return result

def last(iterable, default=None):
    """Try to get the last iterable item by successive iteration on it."""

    result = default

    iterator = iter(iterable)

    while True:
        try:
            result = next(iterator)

        except StopIteration:
            break

    return result

def itemat(iterable, index):
    """Try to get the item at index position in iterable after iterate on
    iterable items."""

    result = None

    iterator = iter(iterable)

    if index < 0:  # ensure index is positive
        index += len(iterable)

    while index >= 0:
        try:
            value = next(iterator)

        except StopIteration:
            break

        else:
            if index == 0:
                result = value
                break
            index -= 1

    return result

def slice(iterable, lower=0, upper=maxsize):
    """Apply a slice on input iterable."""

    if isinstance(iterable, (str, list, tuple)):
        result = iterable[lower, upper]

    else:
        values = []

        if lower < 0:  # ensure lower is positive
            lower += len(iterable)

        if upper < 0:  # ensure upper is positive
            upper += len(iterable)

        if upper > lower:
            iterator = iter(iterable)

            for index in range(0, lower + upper):
                try:
                    value = next(iterator)

                except StopIteration:
                    break

                else:
                    if index >= lower:
                        values.append(value)

        if isinstance(iterable, dict):
            result = {}

            for value in values:
                result[value] = iterable[value]

        else:
            iterablecls = iterable.__class__
            try:
                result = iterablecls(values)

            except:
                result = values

    return result
