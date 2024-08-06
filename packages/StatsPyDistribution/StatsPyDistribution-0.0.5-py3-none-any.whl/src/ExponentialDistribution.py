from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class ExponentialDistribution(Distributions):

    def distribution_family(self):
        return DistributionFamilyType.Continuous.value

    def frequency_density_formula(self):
        return super()._fx_Name+"θ*e^(-θ*x)"

    def name(self):
        return "Exponential Distribution"

    def notation(self):
        return 'expo (θ)'

    def parameters(self):
        return ["0 <= x < ∞", "θ > 0"]

    def __init__(self, theta, size=None):

        if isinstance(theta, str):
            raise Exception("theta must be non string type")

        if size is None:
            size = 10
        if theta is None or theta <= 0:
            raise Exception('A variance(' + str(theta) + ') cannot be negative or zero')
        if not isinstance(size, int):
            raise Exception('Size must be int type')
        if size < 2:
            raise Exception('Size (' + str(size) + ') is not valid. it must be more than one')

        self.__theta = theta
        self.__mn = 1/theta
        self.__var = 1/(theta*theta)
        self.__size = size
        self.__x = [float(i / 10) for i in range(0, 10 * int(size)+1)]
        self.__y = [self._fx_(i) for i in self.__x]
        self.__mgf = [self._mg_function_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__skw = 2
        self.__krt = 6
        self.__mod = 0
        self.__med = math.log(2)/theta

        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        d = {'theta': self.__theta}
        n = self.name() + str(d)
        return n

    def _fx_(self, x):
        return self.__theta*math.exp(-1*self.__theta*x)

    def _mg_function_(self, x):
        if x < self.__theta:
            return self.__theta/(self.__theta - x)
        else:
            return 0

    def _cfx_(self, x):
        return 1 - math.exp(-1*x*self.__theta)

