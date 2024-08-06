from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class TriangularDistribution(Distributions):
    _c = 0

    def probability_random_number(self, x):
        if isinstance(x, str):
            raise Exception("x must be non string type")
        if not self.__a <= x <= self.__b:
            raise Exception("x({}) must be between a({}) and b({}).".format(x, self.__a, self.__b))
        if self.__b - self.__a == 1:
            return self._fx_(x)/2
        else:
            return self._fx_(x)

    def __init__(self, a, b):
        if isinstance(a, str):
            raise Exception("a must be non string type")
        if isinstance(b, str):
            raise Exception("b must be non string type")
        if not a < b:
            raise Exception("a({}) must be less than b({})".format(a, b))
        if self._c == 0:
            self._c = 2 / (b - a)
        c = self._c
        self.__a = a
        self.__b = b
        self.__c = c
        self.__mn = (a + b + c) / 3
        if c >= (a + b) / 2:
            self.__med = a + math.sqrt((b - a) * (c - a) / 2)
        else:
            self.__med = b - math.sqrt((b - a) * (b - c) / 2)
        self.__mod = self.__c
        abc2 = a * a + b * b + c * c - a * b - a * c - b * c
        self.__var = abc2 / 18
        self.__skw = math.sqrt(2) * (a + b - 2 * c) * (2 * a - b - c) * (a - 2 * b + c) / (5 * math.pow(abc2, 3 / 2))
        self.__krt = -3 / 5
        self.__x = [float(i / 10) for i in range(10 * int(a), 10 * int(b)+1)]
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
        d = {'a': self.__a, 'b': self.__b, 'c': self.__c}
        n = self.name() + str(d)
        return n

    def name(self):
        return "Triangular Distribution"

    def frequency_density_formula(self):
        return [super()._fx_Name + "2*(x-a)/((b-a)*(c-a)), if a<x<c", super()._fx_Name + "2/(b-a) if x=c",
                super()._fx_Name + "2*(b-x)/((b-a)*(b-c)) if c<x<b"]

    def notation(self):
        return "Trg.(a,b)"

    def parameters(self):
        return ["-∞ < a < b < ∞"]

    def distribution_family(self):
        return DistributionFamilyType.Continuous.value

    def _fx_(self, x):
        if self.__a <= x < self.__c:
            fx = 2 * (x - self.__a) / ((self.__b - self.__a) * (self.__c - self.__a))
        elif x == self.__c:
            fx = 2/(self.__b-self.__a)
        else:
            fx = 2 * (self.__b - x) / ((self.__b - self.__a) * (self.__b - self.__c))
        return fx

    def _cfx_(self, x):
        if x <= self.__a:
            fx = 0.0
        elif self.__a < x <= self.__c:
            fx = (x - self.__a)*(x - self.__a) / ((self.__b - self.__a) * (self.__c - self.__a))
        elif self.__c < x < self.__b:
            fx = 1 - (self.__b - x)*(self.__b - x) / ((self.__b - self.__a) * (self.__b - self.__c))
        else:
            fx = 1
        return fx

    def _mg_function_(self, x):
        if self.__a == self.__c or self.__c == self.__b:
            return (math.exp(x * self.__b) - math.exp(x * self.__a)) / x * (self.__b - self.__a)
        else:
            exa = math.exp(x * self.__a)
            exb = math.exp(x * self.__b)
            exc = math.exp(x * self.__c)
            bc = self.__b - self.__c
            ba = self.__b - self.__a
            ca = self.__c - self.__a
            return 2 * (bc * exa - ba * exc + ca * exb) / (x * x * bc * ba * ca)
