"""
Singleton functions as a metaclass for singleton objects.

To make all instances of a class a singleton you can do:

    class Base(metaclass=Singleton):
        pass

This is from
https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, new=False, **kwargs):
        if new or cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]
