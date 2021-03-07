import math
from decimal import Decimal

from NIM.benchmarks import Benchmark
from numpy import zeros, pi, cos, exp, sqrt, array
import numpy as np


# double source
class MultiSourceFunction(Benchmark):
    def __init__(self, lower=(0, 0, 0), upper=(20, 20, 0), dimension=3, pg_stability="F", u=2, q=1500, z=1,
                 x0=3.26, y0=9, x1=8.46, y1=16.5):
        super().__init__(lower, upper, dimension)
        self.pg_stability = pg_stability
        self.q0 = q
        self.q1 = q
        self.z = z
        self.x0 = x0
        self.y0 = y0
        self.z0 = z
        self.x1 = x1
        self.y1 = y1
        self.z1 = z
        self.u0 = u
        self.u1 = u
        self.d = 1

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
        result = 0
        if abs(self.y0 - sol[1]) < abs(self.y1 - sol[1]):
            if sol[0] < self.x0:
                result = 0
            else:
                result = self.calculate_concentration(sol[0], sol[1], self.z0, self.q0, self.x0, self.y0, self.z0,
                                                      self.u0, self.pg_stability)
        else:
            if sol[0] < self.x1:
                result = 0
            else:
                result = self.calculate_concentration(sol[0], sol[1], self.z0, self.q1, self.x1, self.y1, self.z1,
                                           self.u1, self.pg_stability)
        return round(result, 4)

    def get_optimum(self):
        return array([[3.3, 9.0],
                      [8.5, 16.5]]), self.q0


if __name__ == '__main__':
    ssf = MultiSourceFunction()

