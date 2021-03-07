import abc

import numpy
from numpy import asarray, random, where, pi, cos, exp, sqrt, full, zeros, array, arange, around, math, ndarray, shape, \
    apply_along_axis
import pandas as pd
import logging

from sklearn.cluster import KMeans

logging.basicConfig(format='%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger('Algorithm')
logger.setLevel('INFO')


class Algorithm(metaclass=abc.ABCMeta):

    def __init__(self, map2d, cell_size, **kwargs):
        """
        debug:      [True|False]: Show  process of each generation
        func:       [Benchmark]:  Function for calculating
        population: [int]:        Population size
        iterations: [int]:        Count of iteration
        precision:  [float]:      Precision of best_value for stopping criteria
        Rand:                     RandomState with seed=1 by default
        lower & upper:            Boundary of function
        dim:                      Dimension of function
        iter:                     Current Iteration started from 0
        eval_count:               Count of cost function called
        """
        self.debug = kwargs.pop('debug', False)
        self.func = kwargs.pop('func', Ackley())
        self.population = kwargs.pop('population', 10)
        self.iterations = kwargs.pop('iterations', 20)
        self.precision = kwargs.pop('precision', 1e-2)
        self.robot_size = kwargs.pop('robot_size', [(0.5, 0.5)] * self.population)
        self.Rand = random.RandomState(kwargs.pop('seed', 5))  # random generator
        self.lower, self.upper = asarray(self.func.lower), asarray(self.func.upper)
        # self.lower, self.upper = asarray(-100), asarray(100)
        self.dim = self.func.dimension
        self.iter = 0
        self.eval_count = 0
        self.stopping_eval = kwargs.pop('stopping_eval', 200)

        self.k = kwargs.pop('k', 4)  # number of leak source

        # Use pandas to save csv conveniently
        # self.best_solution: [dim1, dim2, ..., dimN, Fitness]
        self.best_solution = pd.Series(index=arange(1, self.dim + 2))
        self.best_solution.rename(index={self.dim + 1: 'Fitness'}, inplace=True)
        # self.iter_solution: [Iteration1:[dim1, dim2, ..., dimN, Fitness], Iteration2:[...], ..., IterationN:[...]]
        self.iter_solution = pd.DataFrame(index=arange(1, self.iterations + 1), columns=arange(1, self.dim + 2))
        self.iter_solution.rename(columns={self.dim + 1: 'Fitness'}, inplace=True)
        # self.iter_swarm_pos: [Iteration1:[Individual1[dim1, dim2, ..., dimN], ..., IndividualN[...]], ..., IterationN:[Individual1[...], ..., IndividualN[...]]]
        index = pd.MultiIndex.from_product([arange(1, self.iterations + 1), arange(1, self.population + 1)],
                                           names=['Iteration', 'Individual'])
        columns = list(range(self.dim))
        self.iter_swarm_pos = pd.DataFrame(index=index, columns=columns)

        # block position
        self.map2d = map2d
        self.cell_size = cell_size / 100
        self.low_boundary = self.round_position(asarray(self.func.lower))
        # block position
        self.block = {}
        # robots' information
        self.robot = {}

        self.map_left_boundary = kwargs.pop('map_left_boundary', self.func.lower[1])
        self.map_top_boundary = kwargs.pop('map_top_boundary', self.func.lower[0])

        self.load_block()

    def round_position(self, position):
        '''
        transform position to preset precision
        :param position: position in each generation
        :return: position after transforming
        '''
        if isinstance(position, tuple):
            return round(position[0], int(math.log(1 / self.cell_size, 10))), round(position[1], int(
                math.log(1 / self.cell_size, 10)))
        else:
            return around(position, int(math.log(1 / self.cell_size, 10)))

    def load_block(self):
        '''
        read data of obstacle
        :return: None
        '''
        for i in range(len(self.map2d)):
            for j in range(len(self.map2d[-1])):
                if self.map2d[i][j] == 1:
                    self.block[
                        (self.round_position(self.low_boundary[0] + self.cell_size * i),
                         self.round_position(self.low_boundary[1] + self.cell_size * j))] = 1

    def cal_occupation(self, current, i):
        '''
        set occupation
        :param current:
        :param i: robot index
        :return: occupied position
        '''
        p = []
        size = [int(self.robot_size[i][0] * 2), int(self.robot_size[i][1] * 2)]
        for v in range(size[0]):
            for h in range(size[1]):
                p.append(self.round_position((current[0] + v * self.cell_size, current[1] + h * self.cell_size)))
        return p

    def check_robot(self, current, pos, i):
        '''
        check overlapping with each robot
        :param current: current position
        :param pos: overlapping position
        :param i: index
        :return: whether occupied
        '''
        for item in self.cal_occupation(current, i):
            if (item[0], item[1]) in pos.keys() or (item[0], item[1]) in self.block.keys():
                return False
        return True

    def calculate(self, j):
        '''
        calculate increment
        eg: element in (-1,1,-2,2,-3,3....)
        :param j: index
        :return: increment
        '''
        return int(pow(-1, j) * (j - 0.5 + 0.5 * pow(-1, j)) / 2) * self.cell_size

    def calculate_nearby_position(self, j, k, current_pos):
        '''
        check nearby position
        :param j:
        :param k: (j, k) in scene data
        :param current_pos: current overlapping position
        :return:
        '''
        t = self.round_position((current_pos[0] + self.calculate(j + 1), current_pos[1] + self.calculate(k + 1)))
        return t[0], t[1], current_pos[-1]

    def convert_position_in_each_iter(self, position):
        '''
        handle overlapping
        :param position: current overlapping position
        :return: unoccupied position after handling
        '''
        pos = {}
        for i in range(shape(position)[0]):
            if self.check_robot(position[i], pos, i):
                for item in self.cal_occupation(position[i], i):
                    pos[(item[0], item[1])] = 1
            else:
                current_pos = position[i]
                flag = False
                for count in range(1, len(self.map2d) + 1):
                    for j in range(count):
                        for k in range(count):
                            replace_position = self.calculate_nearby_position(j, k, current_pos)
                            replace_position = self.boundary_handle(array(replace_position))
                            replace_position = tuple(replace_position.tolist())
                            if self.check_robot(replace_position, pos, i):
                                for item in self.cal_occupation(replace_position, i):
                                    pos[(item[0], item[1])] = 1
                                flag = True
                                position[i] = array(replace_position)
                                break
                        if flag:
                            break
                    if flag:
                        break
        return position

    def initial_position(self):
        return self.Rand.uniform(self.lower, self.upper, [self.population, self.func.dimension])

    def boundary_handle(self, x):
        r"""Put the solution in the bounds of problem.
        :param x: Solution to boundary handle
        :return: Bound solution within the search space
        """
        try:
            ir = where(x < self.lower)
            x[ir] = self.lower[ir]
            ir = where(x > self.upper)
            x[ir] = self.upper[ir]
        except Exception as e:
            print(e)
        # ir = where(x < self.lower)
        # x[ir] = self.round_position(self.lower[ir])
        # ir = where(x > self.upper)
        # x[ir] = self.round_position(self.upper[ir])
        return x

    def cost_function(self, position):
        self.eval_count += 1
        return self.func.eval(position)

    def stopping_criteria(self, i):
        return i >= self.iterations

    def stopping_criteria_precision(self, i, optimum_now):
        if i >= self.stopping_eval:
            return True
        if abs(optimum_now - self.func.get_optimum()[-1]) <= self.precision:
            return True
        return False

    def stopping_criteria_eval(self):
        # return self.eval_count >= self.stopping_eval
        return self.iter >= self.iterations

    @abc.abstractmethod
    def run(self):
        pass

    def run_return_swarm_pos(self):
        self.run()
        return self.iter_swarm_pos

    def run_return_best_val(self):
        self.run()
        return self.best_solution['Fitness']

    def run_return_convergence(self):
        self.run()
        return self.iter_solution['Fitness']

    def run_return_iter_sol(self):
        self.run()
        return self.iter_solution

    def run_return_eval_count(self):
        self.run()
        return self.eval_count

    def kmeans(self, k, position, fitness):
        pos = KMeans(n_clusters=k).fit(position)
        cluster = pd.DataFrame(pos.labels_, columns=['c'])
        fitness = pd.DataFrame(fitness, columns=['f'])
        position = pd.DataFrame(position)
        result = pd.concat([cluster, fitness, position], axis=1)
        return cluster, fitness, position, result


class Ackley:

    def __init__(self, lower=-32.768, upper=32.768, dimension=2):
        self.dimension = dimension
        self.lower = full(self.dimension, lower)
        self.upper = full(self.dimension, upper)

    def get_optimum(self):
        return array([zeros(self.dimension)]), 0.0

    @staticmethod
    def eval(sol):
        a = 20
        b = 0.2
        c = 2 * pi
        d = len(sol)

        sum1 = 0.0
        sum2 = 0.0
        for i in range(d):
            xi = sol[i]
            sum1 += xi ** 2
            sum2 += cos(c * xi)
        part1 = -a * exp(-b * sqrt(sum1 / d))
        part2 = -exp(sum2 / d)

        return part1 + part2 + a + exp(1)
