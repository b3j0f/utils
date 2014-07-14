#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ensure str are unicodes
from __future__ import unicode_literals

from inspect import ismodule


def resolve_path(path):
    """
    Get element reference from input full path element.

    :limitations: does not resolve class methods or relative path or with
    wildcard.

    :param path: full path to a python element.
        Examples:
            - __builtin__.open => open builtin function
            - b3j0f.utils.path.resolve_path => this resolve_path function
    :type path: str

    :return: python object which is accessible through input path
        or None if the path can not be resolved
    :rtype: object
    """

    result = None

    if len(path) > 0:

        components = path.split('.')

        module_name = components[0]

        # try to import the first component name
        try:
            result = __import__(module_name)
        except ImportError:
            pass

        if result is not None:

            # try to import all sub-modules/packages
            if len(components) > 1:

                try:  # check if name is defined from an external module
                    # find the right module

                    for index in range(1, len(components)):
                        module_name = '%s.%s' % (
                            module_name, components[index])
                        result = __import__(module_name)

                except ImportError:
                    pass

            # path its content
            for comp in components[1:]:
                result = getattr(result, comp)

    return result


def get_path(element):
    """
    Get full path of a given element such as the opposite of the
    resolve_path behaviour.

    :param element: must be directly defined into a module or a package and has
        the attribute '__name__'
    :type element: object

    :raises: AttributeError in case of element has not the attribute __name__
    """

    if not hasattr(element, '__name__'):
        raise AttributeError(
            'element %s must have the attribute __name__' % element)

    result = element.__name__ if ismodule(element) else \
        '%s.%s' % (element.__module__, element.__name__)

    return result
