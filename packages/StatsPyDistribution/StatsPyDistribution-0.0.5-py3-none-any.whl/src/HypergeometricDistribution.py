from src import DistributionFamilyType
from src.Distributions import Distributions
import math


class HypergeometricDistribution(Distributions):

    def distribution_family(self):
        return DistributionFamilyType.Discrete.value

    def frequency_density_formula(self):
        return super()._fx_Name + "KCk*(N-K)C(n-k)/NCn"

    def name(self):
        return "Hypergeometric Distribution"

    def notation(self):
        return "Hypergeometric(N,K,n)"

    def parameters(self):
        return ["0 <= N < ∞", "0 <= K <= N", "0 <= n < N"]

    def _cfx_(self, x):
        cfx = [self._fx_(int(i)) for i in range(0, x)]
        return sum(cfx)

    def __init__(self, N, K, size=None):
        """
        :param N:
        :Int N:
        :param K:
        :Int K:
        :param size:
        :int size:
        """
        self.K = K
        self.N = N
        if not isinstance(N, int):
            raise Exception("N must be int type")
        if not isinstance(K, int):
            raise Exception("K must be int type")
        if not isinstance(size, int):
            raise Exception("size must be int type")
        if size is None:
            size = N
        if N is None or N < 0:
            raise Exception('N(' + str(N) + ') cannot be negative or zero')
        if K is None or K < 0:
            raise Exception('K(' + str(K) + ') cannot be negative or zero')
        if K > N:
            raise Exception(f'K({K}) must be b/w 0 to N({N})')
        if size > N:
            raise Exception(f'size or n({size}) must be b/w 0 to N({size})')

        self.__mn = size * K / N
        self.__var = size * K * (N - K) * (N - size) / (N * N * (N - 1))
        self.__size = size
        self.__x = range(max(0, size + K - N), min(size, K))
        self.__y = [self._fx_(i) for i in self.__x]
        self.__cdf = [self._cfx_(i) for i in self.__x]
        self.__mgf = [self._mg_function_(i) for i in self.__x]
        self.__skw = float("inf")
        self.__krt = float("inf")
        self.__mod = math.floor((size + 1) * (K + 1) / (N + 2))
        self.__med = float("inf")

        Distributions.__init__(self, x=self.__x, y=self.__y, m=self.__mn, v=self.__var, mo=self.__mod, me=self.__med,
                               sk=self.__skw, kr=self.__krt, cdf=self.__cdf, mgf=self.__mgf)

    def __str__(self):
        d = {'K': self.K, 'N': self.N, 'n': self.__size}
        n = self.name() + str(d)
        return n

    def _fx_(self, x):
        n = self.__size
        if not (max(0, n + self.K - self.N) <= x <= min(n, self.K)):
            raise Exception(f"X:{x} is more than size of distribution from {max(0, n + self.K - self.N)} to {min(n, self.K)}")
        return math.comb(self.K, x) * math.comb((self.N - self.K), (n - x)) / math.comb(self.N, n)

    def _mg_function_(self, x):
        n = self.__size
        if not (max(0, n + self.K - self.N) <= x <= min(n, self.K)):
            raise Exception(
                f"X:{x} is more than size of distribution from {max(0, n + self.K - self.N)} to {min(n, self.K)}")
        return math.perm(self.K, x) * math.perm(n, x) / math.perm(self.N, x)
