#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ensure str are unicodes
from __future__ import unicode_literals

from inspect import ismodule, currentframe

from importlib import import_module


def resolve_path(path):
    """
    Get element reference from input full path element.

    :limitations: it does not resolve class methods or relative path or with
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

    if path:

        components = path.split('.')
        index = 0
        components_len = len(components)

        module_name = components[0]

        # try to import the first component name
        try:
            result = import_module(module_name)
        except ImportError:
            pass

        if result is not None:

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
                        raise Exception(
                            'Wrong path %s at %s' % (path, components[:index]))

        else:  # get relative object from current module

            raise Exception('Does not handle relative path')

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
