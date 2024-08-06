from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class GeometricDistribution(Distributions):

    def distribution_family(self):
        return DistributionFamilyType.Discrete.value

    def frequency_density_formula(self):
        return super()._fx_Name+"p*(1 - p)^k"

    def name(self):
        return "Geometric Distribution"

    def notation(self):
        return "GD(p)"

    def parameters(self):
        return ["0 < p <= 1"]

    def _cfx_(self, x):
        cfx = [self._fx_(int(i)) for i in range(0, x)]
        return sum(cfx)

    def __init__(self, probability):
        """
        :param probability:
        :float probability:
        """
        if isinstance(probability, str):
            raise Exception("probability must be non string type")

        if probability is None or probability <= 0:
            raise Exception('A probability(' + str(probability) + ') cannot be negative or zero')
        if probability > 1.0:
            raise Exception('A probability(' + str(probability) + ') cannot be more than 1')

        size = 20
        self.__mn = 1/probability
        self.__var = probability/(1 - probability * probability)
        self.__size = size
        self.__x = range(0, size)
        self.__y = [self._fx_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__mgf = [self._mg_function_(i) for i in self.__x]
        self.__skw = (2 - probability)/math.sqrt((1 - probability))
        self.__krt = 6 + probability * probability/(1 - probability)
        self.__mod = 1
        self.__med = math.ceil(-1/math.log2(1 - probability))

        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        p = {'p': 1/self.__mn}
        n = self.name() + " " + str(p)
        return n

    def _fx_(self, x):

        p = 1/self.__mn
        q = 1 - p
        return self.pow(q, x) * p

    def pow(self, v, n):
        try:
            result = math.exp(n * math.log(v))
            return result
        except OverflowError:
            return float('inf')

    def _mg_function_(self, x):
        p = 1 / self.__mn
        q = 1 - p
        return p * self.pow(math.e, x) / (1 - q * self.pow(math.e, x))
