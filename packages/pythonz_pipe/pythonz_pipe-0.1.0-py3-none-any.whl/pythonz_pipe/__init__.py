__all__ = ['pipe']
__version__ = '0.1.0'


class Pipe:
    __empty__ = object()

    def __init__(self, it=__empty__, f=lambda x: x) -> None:
        self.it = it
        self.f = f

    def unwrap(self):
        if self.it is self.__empty__:
            raise ValueError("Cannot unwrap an empty pipe")
        return self.f(self.it)

    def call(self, it):
        if self.it is not self.__empty__:
            raise ValueError("Cannot call a non-empty pipe")
        return self.f(it)

    def and_then(self, f):
        cls = self.__class__
        return cls(self.it, lambda x: f(self.f(x)))

    def then_finally(self, f):
        return self.and_then(f).unwrap()

    def __call__(self, it):
        return self.call(it)

    def __truediv__(self, other):
        if not callable(other):
            raise NotImplementedError("Cannot pipe a non-callable object")
        return self.and_then(other)

    def __floordiv__(self, other):
        if not callable(other):
            raise NotImplementedError("Cannot pipe a non-callable object")
        return self.then_finally(other)


pipe = Pipe
