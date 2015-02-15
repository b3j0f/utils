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

__all__ = ['get_proxy']

"""Module in charge of creating proxies.
"""

from functools import wraps

from types import MethodType

from inspect import getmembers, isroutine, isfunction, ismethod, getargspec

from abc import ABCMeta

from b3j0f.utils.version import PY2, basestring
from b3j0f.utils.path import lookup

#: list of attributes to set after wrapping a function with a joinpoint
WRAPPER_ASSIGNMENTS = ['__doc__', '__module__', '__name__']
WRAPPER_UPDATES = ['__dict__']


class ProxyMeta(ABCMeta):
    """Meta class for proxy elements.
    """

    def __call__(cls, elt, bases=None, content=None, *args, **kwargs):
        """A proxy may be called with base types and a reference to an
        elt.

        :param cls: cls to instantiate.
        :param elt: elt to proxify.
        :param bases: If not None, base types to proxify.
        :param content: If not None, class members to proxify.
        """

        result = super(ProxyMeta, cls).__call__(*args, **kwargs)
        # init content
        content = {} if content is None else content
        # enrich proxy with bases
        if bases is not None:
            # ensure bases is a set of types
            if isinstance(bases, basestring):
                bases = [lookup(bases)]
            elif issubclass(bases, type):
                bases = [bases]
            else:  # convert all str to type
                bases = [
                    base if issubclass(base, type) else lookup(base)
                    for base in bases
                ]
            # enrich cls with base types
            for base in bases:
                # register base in cls
                cls.register(base)
                # enrich methods/functions
                for name, member in getmembers(
                    base, lambda member: isroutine(member)
                ):
                    if name not in content:
                        content[name] = member

        # enrich proxy with content
        for name in content:
            if not hasattr(cls, name):
                value = content[name]
                proxy = ProxyMeta.proxify_routine(
                    value, elt=elt, name=name
                )
                if proxy is not None:
                    setattr(cls, name, proxy)

        return result

    @staticmethod
    def proxify_routine(target, elt=None, name=None):

        @wraps(target)
        def result(*args, **kwargs):
            if elt is None:
                result = target(*args, **kwargs)
            else:
                result = getattr(elt, name)(*args, **kwargs)

            return result

        return result

# create proxy class
if PY2:
    class Proxy(object):
        __metaclass__ = ProxyMeta

else:
    # compile Proxy class on the fly because it is not PY2 syntaxically correct
    codestr = "class Proxy(object, metaclass=ProxyMeta): pass\n"
    code = compile(codestr, __file__, 'single')
    exec(code, globals())
# set docstring to proxy class
Proxy.__doc__ = "Proxy class"


def get_proxy(elt, bases=None, content=None):
    """Get proxified elt.

    :param elt: elt to proxify.
    :type elt: object or function/method
    :param bases: base types to enrich in the result cls if not None.
    :param content: class members to proxify if not None.
    """

    if isfunction(elt):
        result = ProxyMeta.proxify_routine(elt)

    elif ismethod(elt):
        function = ProxyMeta.proxify_routine(elt)
        args = [function, elt]
        if PY2:  # add class to args in PY2
            args.append(elt.__class__)
        result = MethodType(*args)

    else:  # in case of object, result is a Proxy
        result = Proxy(elt, bases=bases, content=content)

    return result
