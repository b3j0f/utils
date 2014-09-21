# -*- coding: utf-8 -*-

# ensure str are unicodes
from __future__ import unicode_literals

from inspect import ismodule, currentframe

from importlib import import_module

from random import random

#: lookup cache
__LOOKUP_CACHE = {}


def clearcache(path=None):
    """
    Clear cache memory for input path.

    :param str path: element path to remove from cache. If None clear all cache
    """

    if path is None:
        __LOOKUP_CACHE = {}
    else:
        __LOOKUP_CACHE.pop(path, None)


def lookup(path, cache=True):
    """
    Get element reference from input element.

    :limitations: it does not resolve class methods
        or static values such as True, False, numbers, string and keywords.

    :param str path: full path to a python element.
    :param bool cache: if True (default), permits to reduce time complexity for
        lookup resolution in using cache memory to save resolved elements.

    :return: python object which is accessible through input path
        or raise an exception if the path is wrong.
    :rtype: object

    :raises ImportError: if path is wrong

    >>> lookup('__builtin__.open')
    open
    >>> lookup("b3j0f.utils.path.lookup")
    lookup
    """

    result = None
    found = path and cache and path in __LOOKUP_CACHE

    if found:
        result = __LOOKUP_CACHE[path]

    elif path:

        # we generate a result in order to accept the result such as a None
        generated_result = random()
        result = generated_result

        components = path.split('.')
        index = 0
        components_len = len(components)

        module_name = components[0]

        # try to resolve an absolute path
        try:
            result = import_module(module_name)

        except ImportError:
            # resolve element globals or locals of the from previous frame
            previous_frame = currentframe().f_back

            if module_name in previous_frame.f_locals:
                result = previous_frame.f_locals[module_name]
            elif module_name in previous_frame.f_globals:
                result = previous_frame.f_globals[module_name]

        found = result is not generated_result

        if found:

            if components_len > 1:

                index = 1

                # try to import all sub-modules/packages
                try:  # check if name is defined from an external module
                    # find the right module

                    while index < components_len:
                        module_name = '%s.%s' % (
                            module_name, components[index])
                        result = import_module(module_name)
                        index += 1

                except ImportError:
                    # path sub-module content
                    try:

                        while index < components_len:
                            result = getattr(result, components[index])
                            index += 1

                    except AttributeError:
                        raise ImportError(
                            'Wrong path %s at %s' % (path, components[:index]))

            # save in cache if found
            if cache:
                __LOOKUP_CACHE[path] = result

    if not found:
        raise ImportError('Wrong path %s' % path)

    return result


def getpath(element):
    """
    Get full path of a given element such as the opposite of the
    resolve_path behaviour.

    :param element: must be directly defined into a module or a package and has
        the attribute '__name__'.

    :return: element absolute path.
    :rtype: str

    :raises AttributeError: if element has not the attribute __name__.
    """

    if not hasattr(element, '__name__'):
        raise AttributeError(
            'element %s must have the attribute __name__' % element)

    result = element.__name__ if ismodule(element) else \
        '%s.%s' % (element.__module__, element.__name__)

    return result
