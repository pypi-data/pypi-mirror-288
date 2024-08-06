from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class BinomialDistribution(Distributions):

    def distribution_family(self):
        return DistributionFamilyType.Discrete.value

    def frequency_density_formula(self):
        return super()._fx_Name+"nCk*p^k*(1-p)^k"

    def name(self):
        return "Binomial Distribution"

    def notation(self):
        return "B(n,p)"

    def parameters(self):
        return ["0 <= p <= 1",  "0 <= n < ∞"]

    def _cfx_(self, x):
        cfx = [self._fx_(int(i)) for i in range(0, x)]
        return sum(cfx)

    def __init__(self, probability, size=None):
        """
        :param probability:
        :float probability:
        :param size:
        :int size:
        """
        if isinstance(probability, str):
            raise Exception("probability must be non string type")

        if size is None:
            size = 10
        if probability is None or probability < 0:
            raise Exception('A probability(' + str(probability) + ') cannot be negative or zero')
        if probability is None or probability > 1.0:
            raise Exception('A probability(' + str(probability) + ') cannot be more than 1')
        if not isinstance(size, int):
            raise Exception('Size must be int type')
        if size < 2:
            raise Exception('Size (' + str(size) + ') is not valid. it must be more than one')

        self.__mn = size * probability
        self.__var = size * probability * (1 - probability)
        self.__size = size
        self.__x = range(0, size)
        self.__y = [self._fx_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__mgf = [self._mg_function_(i) for i in self.__x]
        self.__skw = (1 - 2 * probability)/math.sqrt(size*(1 - probability)*probability)
        self.__krt = (1 - 6 * probability * (1-probability))/(size*(1 - probability)*probability)
        self.__mod = math.floor((size - 1)*probability)
        self.__med = math.floor(self.__mn)

        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        d = {'p': self.__mn/self.__size, 'n': self.__size}
        n = self.name() + str(d)
        return n

    def _fx_(self, x):
        n = self.__size
        if x > n:
            raise Exception(f"X:{x} is more than size of distribution :{n} ")
        p = self.__mn/self.__size
        return math.comb(n, x) * math.pow(p, x) * math.pow((1 - p), (n - x))

    def safe_pow(self,v, n):
        try:
            result = math.exp(n * math.log(v))
            return result
        except OverflowError:
            return float('inf')

    def _mg_function_(self, x):
        n = self.__size
        if x > n:
            raise Exception(f"X:{x} is more than size of distribution :{n} ")

        p = self.__mn / self.__size
        q = 1 - p
        v = q + p * math.exp(x)
        return self.safe_pow(v, n)
