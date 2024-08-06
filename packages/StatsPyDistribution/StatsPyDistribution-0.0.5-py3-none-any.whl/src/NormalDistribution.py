from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class NormalDistribution(Distributions):

    def distribution_family(self):
        return DistributionFamilyType.Continuous.value

    def frequency_density_formula(self):
        return super()._fx_Name+"e^(-((x-μ)/σ)\u00B2/2)/(\u03C3\u221A(2\u03C0))"

    def name(self):
        return "Normal Distribution"

    def notation(self):
        return '\u039D(\u03BC,\u03C3\u00B2)'

    def parameters(self):
        return ["-∞ < x < ∞", "-∞ < μ < ∞", "0 < σ < ∞"]

    def _cfx_(self, x):
        return (1+math.erf((x - self.__mn)/(self.__var * math.sqrt(2))))/2

    def __init__(self, mean, var, size=None):
        """
        :param mean:
        :float mean:
        :param var:
        :float var:
        :param size:
        :int size:
        """
        if isinstance(var, str):
            raise Exception("var must be non string type")

        if isinstance(mean, str):
            raise Exception("mean must be non string type")
        if size is None:
            size = 10
        if var is None or var <= 0:
            raise Exception('A variance(' + str(var) + ') cannot be negative or zero')
        if not isinstance(size, int):
            raise Exception('Size must be int type')
        if size < 2:
            raise Exception('Size (' + str(size) + ') is not valid. it must be more than one')

        self.__mn = mean
        self.__var = var
        self.__size = size
        self.__x = [float(i / 10) for i in range(10 * (0 - int(size / 2)), 10 * (1 + int(size / 2)))]
        self.__y = [self._fx_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__mgf = [self._mg_function_(i) for i in self.__x]
        self.__skw = 0
        self.__krt = 0
        self.__mod = mean
        self.__med = mean

        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        d = {'mean': self.__mn, 'var': self.__var, 'size': self.__size}
        n = self.name() + str(d)
        return n

    def _fx_(self, x):
        return math.exp(-1 * math.pow(x - self.__mn, 2) / (2 * math.pow(self.__var, 2))) \
               / (self.__var * math.sqrt(2 * math.pi))

    def _mg_function_(self, x):
        return math.exp(self.__mn * x - math.pow(self.__var, 2) * math.pow(x, 2) / 2)
