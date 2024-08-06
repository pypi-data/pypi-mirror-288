from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class RectangularDistribution(Distributions):

    def probability_random_number(self, x):
        if isinstance(x, str):
            raise Exception("x must be non string type")
        if not self.__a <= x <= self.__b:
            raise Exception("x({}) must be between a({}) and b({}).".format(x, self.__a, self.__b))
        return self._fx_(x)

    def __init__(self, a, b):
        if isinstance(a, str):
            raise Exception("a must be non string type")

        if isinstance(b, str):
            raise Exception("b must be non string type")
        if a >= b:
            raise Exception("a({}) must be less than b({})".format(a, b))
        self.__a = a
        self.__b = b
        self.__mn = (a + b) / 2
        self.__mod = "any value b/w a and b"
        self.__med = self.__mn
        self.__var = math.pow(b - a, 2) / 12
        self.__skw = 0
        self.__krt = -6 / 5
        self.__x = [float(i / 10) for i in range(10 * int(a), 10 * int(b) + 1)]
        if self.__x.__contains__(0.0):
            self.__x.remove(0.0)
        self.__y = [self._fx_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__mgf = []
        try:
            self.__mgf = [self._mg_function_(i) for i in self.__x]
        except OverflowError:
            self.__mgf = []
        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        d = {'a': self.__a, 'b': self.__b}
        n = self.name() + str(d)
        return n

    def name(self):
        return "Rectangular( Or Uniform) Distribution"

    def frequency_density_formula(self):
        return [super()._fx_Name + "1/(b-a), if a<x<b", super()._fx_Name + "0, otherwise"]

    def notation(self):
        return "U[a,b]"

    def parameters(self):
        return ["-∞ < a < b < ∞"]

    def distribution_family(self):
        return DistributionFamilyType.Continuous.value

    def _cfx_(self, x):
        if x < self.__b:
            return (x - self.__a) / (self.__b - self.__a)
        else:
            return 1

    def _fx_(self, x):
        return 1 / (self.__b - self.__a)

    def _mg_function_(self, x):
        return (math.exp(x * self.__b) - math.exp(x * self.__a)) / x * (self.__b - self.__a)
