from src.TriangularDistribution import TriangularDistribution


class SymmetricTriangularDistribution(TriangularDistribution):

    def name(self):
        return "Symmetric Triangular Distribution"

    def __init__(self, a, b):
        if isinstance(a, str):
            raise Exception("a must be non string type")
        if isinstance(b, str):
            raise Exception("b must be non string type")
        if not a < b:
            raise Exception("a({}) must be less than b({})".format(a, b))
        self._c = (a+b)/2
        self.__a = a
        self.__b = b
        TriangularDistribution.__init__(self, a, b)

    def __str__(self):
        d = {'a': self.__a, 'b': self.__b, 'c': self._c}
        n = self.name() + str(d)
        return n

    def notation(self):
        return "STrg.(a,b)"

