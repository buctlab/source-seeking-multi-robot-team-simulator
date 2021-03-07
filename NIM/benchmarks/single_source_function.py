from NIM.benchmarks import Benchmark
from numpy import zeros, pi, cos, exp, sqrt, array
import numpy as np


class SingleSourceFunction(Benchmark):
    def __init__(self, lower=(0, 0, 1), upper=(20, 20, 1), dimension=3, pg_stability="F", u=2, q0=1500, x0=3.25,
                 y0=12.211, z0=1):
        super().__init__(lower, upper, dimension)
        self.pg_stability = pg_stability
        self.q0 = q0
        # self.z = z
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.u = u

    @staticmethod
    def sigma_y(pg_stability, x):
        if pg_stability == 'A':
            return 0.22 * x * (1 + 0.0001 * x) ** (-0.5)
        elif pg_stability == 'B':
            return 0.16 * x * (1 + 0.0001 * x) ** (-0.5)
        elif pg_stability == 'C':
            return 0.11 * x * (1 + 0.0001 * x) ** (-0.5)
        elif pg_stability == 'D':
            return 0.08 * x * (1 + 0.0001 * x) ** (-0.5)
        elif pg_stability == 'E':
            return 0.06 * x * (1 + 0.0001 * x) ** (-0.5)
        else:
            return 0.04 * x * (1 + 0.0001 * x) ** (-0.5)

    @staticmethod
    def sigma_z(pg_stability, x):
        if pg_stability == 'A':
            return 0.2 * x
        elif pg_stability == 'B':
            return 0.12 * x
        elif pg_stability == 'C':
            return 0.08 * x * (1 + 0.0002 * x) ** (-0.5)
        elif pg_stability == 'D':
            return 0.06 * x * (1 + 0.0015 * x) ** (-0.5)
        elif pg_stability == 'E':
            return 0.03 * x * (1 + 0.0003 * x) ** (-1)
        else:
            return 0.016 * x * (1 + 0.0003 * x) ** (-1)

    def calculate_concentration(self, x, y, z, q0, x0, y0, z0, u, pg_stability):
        part1 = (q0 / (2 * pi * self.sigma_y(pg_stability, (x - x0)) * self.sigma_z(pg_stability, (x - x0)) * u)) * exp(
            -0.5 * ((y - y0) ** 2) / (self.sigma_y(pg_stability, (x - x0)) ** 2))
        part2 = exp(-((z - z0) ** 2) / (2 * (self.sigma_z(pg_stability, (x - x0)) ** 2))) + exp(
            -((z + z0) ** 2) / (2 * (self.sigma_z(pg_stability, (x - x0)) ** 2)))
        return part1 * part2

    def eval(self, sol):
        if sol[0] < self.x0:
            return 0
        return self.calculate_concentration(sol[0], sol[1], self.z0, self.q0, self.x0, self.y0, self.z0, self.u,
                                            self.pg_stability)

    def get_optimum(self):
        return array([[3.3, 12.2]]), self.q0


if __name__ == '__main__':
    ssf = SingleSourceFunction()
    print(ssf.eval([35.962, 10.87, 2.17]))
# x0=35.96, y0=10.87, z0=2.17
