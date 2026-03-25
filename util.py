from threading import Lock

class SingletonMeta(type):
    """
    Thread-safe singleton metaclass.

    Any class that uses `metaclass=SingletonMeta` will only be instantiated once
    per process; subsequent calls return the same instance.
    """

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]