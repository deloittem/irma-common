import types


##############################################################################
# Singleton Design Pattern
##############################################################################

class SingletonMetaClass(type):
    """Metaclass for singleton design pattern.

    .. warning::

            This metaclass should not be used directly. To declare a class
            using the singleton pattern, one should use the :class:`Singleton`
            class instead.

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# Metaclass compatible with python 2 and 3. Inherit from this for singletons
Singleton = SingletonMetaClass('Singleton', (object, ), {})
"""Base class for singleton

This class implements the singleton design pattern. One can inherit from this
base class to make a class implement the singleton design pattern.

    .. code-block:: python

        # a class implementing a singleton
        class aParametricSingleton(Singleton):
            
            # do some stuff here
            pass

        # let us verify that it is really a singleton
        print(id(aParametricSingleton())
        print(id(aParametricSingleton())

"""

##############################################################################
# Parametric Singleton Design Pattern
##############################################################################

class ParametricSingletonMetaClass(type):
    """Metaclass for parametric singleton design pattern

    .. warning::

            This metaclass should not be used directly. To declare a class
            using the singleton pattern, one should use the
            :class:`ParametricSingleton` class instead and precise the
            parameter used for the dict using a class method named
            ``depends_on``.

    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        # check for "depends_on" attribute
        if not "depends_on" in kwargs and not hasattr(cls, "depends_on"):
            raise TypeError("argument or attribute 'depends_on' not defined")
        # check for unbound methods
        if "depends_on" in kwargs and \
           (not kwargs["depends_on"] or not callable(kwargs["depends_on"])):
            raise TypeError("function in parameter 'depends_on' is not bound")
        elif hasattr(cls, "depends_on") and \
             (not getattr(cls, "depends_on") or not callable(getattr(cls, "depends_on"))):
            raise TypeError("function in attribute 'depends_on' is not bound")

        # call depends_on to get the key
        if "depends_on" in kwargs:
            key = kwargs["depends_on"](cls, args, kwargs)
            del kwargs["depends_on"]
        else:
            key = getattr(cls, "depends_on")(cls, args, kwargs)

        # check for instance
        if key not in cls._instances:
            cls._instances[key] = super(ParametricSingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instances[key]

# Metaclass compatible with python 2 and 3. Inherit from this for parametric singletons
ParametricSingleton = ParametricSingletonMetaClass('ParametricSingleton', (object, ), {})
"""Base class for parametric singletons

This class implements the parametric singleton design pattern. One can inherit
from this base class to make a class implement a parametric singleton pattern.
Pass either an argument ``depends_on`` in the constructor or define a class
method called ``depends_on`` that specifies how to compute the parameter value
used for the hash table storing the instances:

* example with a **static method**:

.. code-block:: python

    class aParametricSingleton(ParametricSingleton):
  
        @staticmethod
        def depends_on(*args, **kwargs):
            return "my key"

* example with a **``lambda`` wrapped with a static method**:

.. code-block:: python
        
    class aParametricSingleton(ParametricSingleton):

        depends_on = staticmethod(lambda *args, **kwargs: "my key")
"""