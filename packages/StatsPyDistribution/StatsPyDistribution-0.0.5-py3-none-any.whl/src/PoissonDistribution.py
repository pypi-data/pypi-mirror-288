from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class PoissonDistribution(Distributions):

    def distribution_family(self):
        return DistributionFamilyType.Discrete.value

    def frequency_density_formula(self):
        return super()._fx_Name+"λ^k*e^-λ/k!"

    def name(self):
        return "Poisson Distribution"

    def notation(self):
        return "Pois(λ)"

    def parameters(self):
        return ["0 <= λ < ∞"]

    def _cfx_(self, x):
        cfx = [self._fx_(int(i)) for i in range(0, x)]
        return sum(cfx)

    def __init__(self, lamda):
        """
        :param lamda:
        :float lamda:
        """
        if isinstance(lamda, str):
            raise Exception("λ:lamda must be non string type")

        if lamda is None or lamda < 0:
            raise Exception('A lamda(' + str(lamda) + ') cannot be negative or zero')

        size = 40
        self.__mn = lamda
        self.__var = lamda
        self.__size = size
        self.__x = range(0, size)
        self.__y = [self._fx_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__mgf = [self._mg_function_(i) for i in self.__x]
        self.__skw = 1/math.sqrt(lamda)
        self.__krt = 1/lamda
        self.__mod = math.floor(lamda)
        self.__med = math.floor(lamda + 1/3 - 1/50*lamda)

        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        d = {'λ': self.__mn}
        n = self.name() + " " + str(d)
        return n

    def _fx_(self, x):
        _lamda = self.__mn
        return self.pow(_lamda, x) * math.pow(math.e, -1*_lamda) / math.factorial(x)

    def pow(self, v, n):
        try:
            result = math.exp(n * math.log(v))
            return result
        except OverflowError:
            return float('inf')

    def _mg_function_(self, x):
        _lamda = self.__mn
        return self.pow(math.e, _lamda*(self.pow(math.e, x) - 1))
