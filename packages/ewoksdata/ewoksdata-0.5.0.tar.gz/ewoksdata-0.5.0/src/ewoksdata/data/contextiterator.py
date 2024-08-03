from collections.abc import Generator


class ContextIterator(Generator):
    def __init__(self, it):
        self._it = it

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._it)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._it.close()

    def send(self):
        return next(self._it)

    def throw(self):
        raise StopIteration


def contextiterator(iterator):
    """Decorator that allows to use an iterator as a context manager.
    This ensures that the iterator is closed when exiting the context manager.
    """

    def wrapper(*args, **kw):
        return ContextIterator(iterator(*args, **kw))

    return wrapper
