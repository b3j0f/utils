from b3j0f.utils.proxy import get_proxy


class A(object):
    def a(self):
        return self

a = A()

pa = get_proxy(a)

print pa.a.__func__ is a.a.__func__
