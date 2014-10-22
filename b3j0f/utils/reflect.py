# -*- coding: utf-8 -*-

"""
Python reflection tools.
"""

from types import NoneType

from inspect import isclass, isroutine, ismethod

__all__ = ['base_elts']


def base_elts(elt, cls=None):
    """
    Get bases elements of the input elt.

    :param elt: supposed inherited elt.
    :param cls: cls from where find attributes equal to elt. If None, it is
        found as much as possible. Required in python3 for function classes.
    :return: elt bases elements. if elt has not base elements, result is empty.
    :rtype: set
    """

    result = set()

    elt_name = getattr(elt, '__name__', None)

    if elt_name is not None:

        # identify type of elt
        if isroutine(elt):  # in case of routine (callable element)

            classes = None  # classes where find base elts

            if cls is None:  # if cls is None, try to find it

                if hasattr(elt, '__self__'):  # from the instance

                    instance = elt.__self__  # get instance

                    if instance is None and hasattr(elt, 'im_class'):
                        # if instance is None, check if class is NoneType
                        if issubclass(elt.im_class, NoneType):
                            classes = (instance.__class__)

                        else:  # else get im_class
                            classes = elt.im_class

                    else:  # use instance class
                        classes = (instance.__class__,)

            else:  # classes is cls

                classes = cls.__bases__

            if classes is not None:  # if cls has been found

                # get an elt to compare with found element
                elt_to_compare = elt.__func__ if ismethod(elt) else elt

                for cls in classes:  # for all classes
                    # get possible base elt
                    b_elt = getattr(cls, elt_name, None)

                    if b_elt is not None:
                        # compare funcs
                        bec = b_elt.__func__ if ismethod(b_elt) else b_elt
                        # if matching, add to result
                        if bec is elt_to_compare:
                            result.add(b_elt)

        elif isclass(elt):  # in case of class
            result = set(elt.__bases__)  # add base classes to the result

    return result
