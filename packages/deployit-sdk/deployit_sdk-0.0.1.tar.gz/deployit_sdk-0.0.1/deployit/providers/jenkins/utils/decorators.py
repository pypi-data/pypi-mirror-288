def make_singleton(cls):
    """
    Decorator to make a class a singleton.

    Ensures that only one instance of the class is created. If an instance
    already exists, it returns the existing instance.

    Parameters
    ----------
    cls : type
        The class to be decorated as a singleton.

    Returns
    -------
    instance : function
        A function that returns the singleton instance of the class.

    Examples
    --------
    >>> @singleton
    ... class MyClass:
    ...     pass
    ...
    >>> obj1 = MyClass()
    >>> obj2 = MyClass()
    >>> obj1 is obj2
    True
    """
    instances = {}
    def instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return instance