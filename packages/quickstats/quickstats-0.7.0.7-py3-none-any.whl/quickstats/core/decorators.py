from typing import Optional, get_type_hints
from functools import partial, wraps
from dataclasses import dataclass, field, fields, Field, MISSING
import sys
import time
import inspect
import importlib

from .type_validation import check_type, get_type_hint_str
from .typing import NOT_SET

__all__ = ["semistaticmethod", "cls_method_timer", "timer", "type_check", "strongdataclass"]

class semistaticmethod(object):
    """
    Descriptor to allow a staticmethod inside a class to use 'self' when called from an instance.

    This custom descriptor class `semistaticmethod` enables a static method defined inside a class 
    to access the instance (`self`) when called from an instance, similar to how regular instance 
    methods can access the instance attributes. By default, static methods do not have access to 
    the instance and can only access the class-level attributes.

    Note:
        When defining a static method using this descriptor, it should be used like a regular method 
        within the class definition. It will work as a normal static method when called from the class, 
        and when called from an instance, it will receive the instance as the first argument.

    Args:
        callable (function): The original static method defined within the class.

    Returns:
        callable: A callable object that behaves like a static method but can also access the instance.
    """
    def __init__(self, callable):
        self.f = callable

    def __get__(self, obj, type=None):
        if (obj is None) and (type is not None):
            return partial(self.f, type)
        if (obj is not None):
            return partial(self.f, obj)
        return self.f

    @property
    def __func__(self):
        return self.f
        
def cls_method_timer(func):
    """
    Decorator function to measure the execution time of a class method.

    The `cls_method_timer` decorator function can be applied to any class method to automatically measure 
    the execution time of the method. When the decorated method is called, it records the start and end 
    times, calculates the time interval, and prints a message with the method name and the execution time.

    Args:
        func (callable): The class method to be decorated.

    Returns:
        callable: The wrapped function with timing functionality.

    Example:
        class MyClass:
            @cls_method_timer
            def my_method(self, n):
                # Some time-consuming computation here
                result = sum(range(n))
                return result

        obj = MyClass()
        obj.my_method(1000000)  # The decorated method will print the execution time
        # Output: "Task MyClass::my_method executed in 0.006 s"

    Note:
        The `cls_method_timer` function should be used as a decorator when defining a class method. 
        When the decorated method is called, it will print the execution time to the console.
    """
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to measure the execution time of the class method.

        This wrapper function records the start time before calling the original method, then calls 
        the original method, and finally calculates and prints the execution time.

        Args:
            self: The instance of the class.
            *args: Variable-length argument list.
            **kwargs: Keyword arguments.

        Returns:
            The result returned by the original method.
        """
        t1 = time.time()
        result = func(self, *args, **kwargs)
        t2 = time.time()
        method_name = f"{type(self).__name__}::{func.__name__}"
        self.stdout.info(f'Task {method_name!r} executed in {(t2 - t1):.3f} s')
        return result

    return wrapper

class timer:    
    """
    Context manager class for measuring the execution time of a code block.

    Example:
        with timer() as t:
            # Perform some time-consuming task here
            time.sleep(2)

        print("Elapsed time:", t.interval)  # outputs: "Elapsed time: 2.0 seconds"

    """
    def __enter__(self):
        """
        Records the start time when entering the context.

        Returns:
            timer: The timer instance itself.
        """
        self.start_real = time.time()
        self.start_cpu = time.process_time()
        return self

    def __exit__(self, *args):
        """
        Calculates the time interval when exiting the context.

        Args:
            *args: Variable-length argument list.

        Returns:
            None
        """
        self.end_cpu = time.process_time()
        self.end_real = time.time()
        self.interval = self.end_real - self.start_real
        self.real_time_elapsed = self.interval
        self.cpu_time_elapsed = self.end_cpu - self.start_cpu

def type_check(func):
    """
    A decorator to enforce type checking on function arguments based on their type hints.

    Parameters
    ----------
    func : Callable
        The function to be decorated.

    Returns
    -------
    Callable
        The decorated function with type checking.

    Raises
    ------
    TypeError
        If an argument does not match its type hint.

    Examples
    --------
    >>> @type_check
    ... def my_function(a: int, b: str, c, *args, **kwargs):
    ...     print(a, b, c, args, kwargs)
    ...
    >>> my_function(10, "hello", 20, 30, 40, key="value")
    10 hello 20 (30, 40) {'key': 'value'}
    >>> my_function(10, 20, "hello")
    Traceback (most recent call last):
        ...
    TypeError: Type check failed for the function "my_function". Argument "b" must be of type str, but got int.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve the function signature
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # Check each argument against its type hint
        for name, value in bound_args.arguments.items():
            if ((name not in sig.parameters) or 
            (sig.parameters[name].annotation == sig.parameters[name].empty)):
                continue
            type_hint = sig.parameters[name].annotation
            if not check_type(value, type_hint):
                type_hint_str = get_type_hint_str(type_hint)
                raise TypeError(f'Type check failed for the function "{func.__qualname__}". '
                                f'Argument "{name}" must be of type {type_hint_str}, '
                                f'but got {type(value).__name__}.')

        return func(*args, **kwargs)
    
    return wrapper



class NOT_SET:
    pass

def strongdataclass(cls):
    """
    A decorator to create a dataclass with strong type checking.

    Parameters
    ----------
    cls : type
        The class to be decorated.

    Returns
    -------
    type
        The decorated class with strong type checking.
    """
    cls = dataclass(cls)
    type_hints = get_type_hints(cls)
    
    for field in fields(cls):
        private_name = f"_{field.name}"
        public_name = field.name
        type_hint = type_hints.get(field.name, NOT_SET)

        # Define the getter
        def getter(self, private_name=private_name):
            return getattr(self, private_name)

        def setter(self, value, private_name=private_name, type_hint=type_hint):
            if (type_hint is not NOT_SET) and (not check_type(value, type_hint)):
                public_name_ = private_name.strip("_")
                type_hint_str = get_type_hint_str(type_hint)
                raise TypeError(f'`{public_name_}` expects type {type_hint_str}, '
                                f'got {type(value).__name__}')
            setattr(self, private_name, value)

        setattr(cls, public_name, property(getter, setter))
    
    return cls

def strongdataclass(cls=None, *args, **kwargs):
    """
    A decorator to create a dataclass with strong type checking.

    Parameters
    ----------
    cls : type
        The class to be decorated.

    Returns
    -------
    type
        The decorated class with strong type checking.
    """
    def wrap(cls):

        cls = dataclass(cls, *args, **kwargs)
        
        type_hints = get_type_hints(cls)
        
        for field in fields(cls):
            private_name = f"_{field.name}"
            public_name = field.name
            type_hint = type_hints.get(field.name, NOT_SET)

            # Define the getter
            def getter(self, private_name=private_name):
                return getattr(self, private_name)

            def setter(self, value, private_name=private_name, type_hint=type_hint):
                if (type_hint is not NOT_SET) and (not check_type(value, type_hint)):
                    public_name_ = private_name.strip("_")
                    type_hint_str = get_type_hint_str(type_hint)
                    raise TypeError(f'`{public_name_}` expects type {type_hint_str}, '
                                    f'got {type(value).__name__}')
                setattr(self, private_name, value)
    
            setattr(cls, public_name, property(getter, setter))

        return cls

    if cls is None:
        return wrap
        
    return wrap(cls)