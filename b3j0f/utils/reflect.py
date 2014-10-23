# -*- coding: utf-8 -*-

"""
Python reflection tools.
"""

from inspect import isclass, isroutine, ismethod, getmodule

try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

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


def find_embedding(elt, embedding=None):
    """
    Try to get elt embedding elements.

    :param embedding: embedding element. Must be have a module.

    :return: a list of [module [,class]*] embedding elements which define elt:
    """

    result = []  # result is empty in the worst case

    # start to get module
    module = getmodule(elt)

    if module is not None:  # if module exists

        visited = set()  # cache to avoid to visit twice same element

        if embedding is None:
            embedding = module

        # list of compounds elements which construct the path to elt
        compounds = [embedding]

        while compounds:  # while compounds elements exist
            # get last compound
            last_embedding = compounds[-1]
            # stop to iterate on compounds when last embedding is elt
            if last_embedding == elt:
                result = compounds  # result is compounds
                break

            else:
                # search among embedded elements
                for name in dir(last_embedding):
                    # get embedded element
                    embedded = getattr(last_embedding, name)

                    try:  # check if embedded has already been visited
                        if embedded not in visited:
                            visited.add(embedded)  # set it as visited

                        else:
                            continue

                    except TypeError:
                        pass

                    else:

                        try:  # get embedded module
                            embedded_module = getmodule(embedded)
                        except Exception:
                            pass
                        else:
                            # and compare it with elt module
                            if embedded_module is module:
                                # add embedded to compounds
                                compounds.append(embedded)
                                # end the second loop
                                break

                else:
                    # remove last element if no coumpound element is found
                    compounds.pop(-1)

    return result
