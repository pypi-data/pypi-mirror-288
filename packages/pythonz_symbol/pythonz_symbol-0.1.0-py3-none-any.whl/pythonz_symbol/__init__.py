__all__ = ['symbol']


class Symbol:
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return super().__repr__().replace('Symbol', f"Symbol({self._name})")


symbol = Symbol
