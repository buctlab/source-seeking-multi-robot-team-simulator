import random
import time

from NIM.algorithms.algorithm import Algorithm, Ackley
from numpy import asarray, zeros, inf, apply_along_axis, where, fabs, floor, argmax, exp, cos, pi, append, array, sqrt
import logging
import pandas as pd

logging.basicConfig()
logger = logging.getLogger('WOA')
logger.setLevel('INFO')


class WhaleOptimizationAlgorithm(Algorithm):

    def __init__(self, map2d, cell_size, **kwargs):
        super().__init__(map2d, cell_size, **kwargs)

    def encircling_prey(self, i, whale_pos, leader_pos, C, A):
        D = fabs(C * leader_pos - whale_pos[i])
        new_whale_pos = leader_pos - A * D
        return new_whale_pos

    def spiral_update_position(self, i, whale_pos, leader_pos, b, l):
        distance = fabs(leader_pos - whale_pos[i])
        new_whale_pos = distance * exp(b * l) * cos(l * 2 * pi) + leader_pos
        return new_whale_pos

    def search_prey(self, i, whale_pos, C, A):
        rand_leader_index = int(floor(len(whale_pos) * self.Rand.rand()))
        X_rand = whale_pos[rand_leader_index]
        D = fabs(C * X_rand - whale_pos[i])
        new_whale_pos = X_rand - A * D
        return new_whale_pos

    def update_position(self, i, whale_pos, leader_pos, a, a2):
        '''
        update generation
        :param i: index
        :param whale_pos: whale position
        :param leader_pos: leader position
        :param a: parameter in algo
        :param a2: parameter in algo
        :return: new generation
        '''
        r1, r2 = self.Rand.rand(), self.Rand.rand()
        A = 2 * a * r1 - a
        C = 2 * r2
        b = 1
        l = (a2 - 1) * self.Rand.rand() + 1
        p = self.Rand.rand()
        if p < 0.5:
            if fabs(A) < 1:
                return self.encircling_prey(i, whale_pos, leader_pos, C, A)
            else:
                return self.search_prey(i, whale_pos, C, A)
        else:
            return self.spiral_update_position(i, whale_pos, leader_pos, b, l)

    def construct_new_whale(self, result, a, a2):
        r"""
        :param result: Clustered whale population
        :param a: a number that decreased from 2 to 0
        :param a2: a number in [-1, 1]
        :return: new whale population, fitness and cluster
        """
        new_whale = []
        new_whale_cluster = []
        new_whale_fit = []
        for name, group in result.groupby('c'):  # 根据c分组
            leader_pos = group['f'].idxmax()  # 获取到f列，并提取该列的最大值索引
            for i in range(len(group)):
                whale = self.update_position(i, result[[0, 1, 2]].values, result.iloc[leader_pos, 2:].values, a, a2)
                whale = self.boundary_handle(asarray(whale))  # 调用algorithm.py中的boundary_handle函数
                new_whale.append(whale)
                new_whale_cluster.append(name)
                new_whale_fit.append(self.cost_function(whale))  # 调用algorithm.py中的constfunction函数
        new_whale_cluster = pd.DataFrame(new_whale_cluster, columns=['c'])  # 根据c列索引创建dataframe
        new_whale_fit = pd.DataFrame(new_whale_fit, columns=['f'])
        new_whale = pd.DataFrame(new_whale)
        return new_whale, new_whale_fit, new_whale_cluster

    def update_solutions(self, new_whale, new_whale_fit, new_whale_cluster, whale, whale_fit, whale_cluster):
        r"""
        :param new_whale: current new whale population
        :param new_whale_fit: the fitness of new whale population
        :param new_whale_cluster: cluster labels of new whale population
        :param whale: previous generation whale population
        :param whale_fit: the fitness of previous generation whale population
        :param whale_cluster: cluster labels of previous generation whale population
        :return: updated whale position
        """
        for i, row in new_whale.iterrows():
            distance_vector = []
            for j, r in whale.iterrows():
                distance_vector.append(sqrt((((row - r) ** 2).values).sum()))
            nearest_whale = distance_vector.index(min(distance_vector))
            if new_whale_fit.iloc[i]['f'] > whale_fit.iloc[nearest_whale]['f']:
                whale_fit.iloc[nearest_whale] = new_whale_fit.iloc[i]
                whale.iloc[nearest_whale] = row
                whale_cluster.iloc[nearest_whale] = new_whale_cluster.iloc[i]
        result = pd.concat([whale_cluster, whale_fit, whale], axis=1)  # 将三个数据垂直方向进行拼接
        return result

    def run(self):
        '''
        seeking according to k value
        :return: source position
        '''
        if self.k == 1:
            return self.run_single_source()
        else:
            return self.run_multi_source()

    def run_multi_source(self):
        whale_pos = pd.DataFrame(self.initial_position())
        whale_fit = whale_pos.apply(self.cost_function, axis=1).astype('float')
        self.iter = 0

        ibest = argmax(whale_fit.values)
        leader_pos, leader_fit = whale_pos.values[ibest], whale_fit.values[ibest]

        converted_pos = apply_along_axis(self.round_position, 1, whale_pos.values)
        converted_pos = self.convert_position_in_each_iter(converted_pos)
        converted_whale_fit = apply_along_axis(self.cost_function, 1, converted_pos)
        converted_ibest = argmax(converted_whale_fit)
        converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_whale_fit[
            converted_ibest]

        while not self.stopping_criteria(self.iter):
            a = 2 - self.iter * (2 / self.iterations)
            a2 = -1 + self.iter * (-1 / self.iterations)
            self.iter += 1
            self.iter_swarm_pos.loc[self.iter] = converted_pos
            self.iter_solution.loc[self.iter] = append(converted_leader_pos, converted_leader_fit)
            if self.debug:
                logger.info("Iteration:{i}/{iterations} - {iter_sol}".format(i=self.iter, iterations=self.iterations,
                                                                             iter_sol=self.iter_solution.loc[
                                                                                 self.iter].to_dict()))
                whale_cluster, whale_fit, whale_pos, result = self.kmeans(self.k, whale_pos, whale_fit)
                new_whale, new_whale_fit, new_whale_cluster = self.construct_new_whale(result, a, a2)
                result = self.update_solutions(new_whale, new_whale_fit, new_whale_cluster,
                                               whale_pos, whale_fit, whale_cluster)
                whale = result[[0, 1, 2]].values
                whale = apply_along_axis(self.boundary_handle, 1, whale)
                whale = apply_along_axis(self.round_position, 1, whale)

                converted_pos = self.convert_position_in_each_iter(whale)
                converted_whale_fit = apply_along_axis(self.cost_function, 1, converted_pos)

                whale_pos = pd.DataFrame(whale)
                whale_fit = whale_pos.apply(self.cost_function, axis=1).astype('float')

                ibest = argmax(whale_fit.values)
                if whale_fit.values[ibest] > leader_fit:
                    leader_pos, leader_fit = whale_pos.values[ibest], whale_fit.values[ibest]

                converted_ibest = argmax(converted_whale_fit)
                if converted_whale_fit[converted_ibest] > converted_leader_fit:
                    converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_whale_fit[
                        converted_ibest]
                print()
        self.best_solution.iloc[:] = append(converted_leader_pos, converted_leader_fit)
        return converted_leader_pos, converted_leader_fit

    def run_single_source(self):
        whale_pos = self.initial_position()
        whale_fit = apply_along_axis(self.cost_function, 1, whale_pos)
        ibest = argmax(whale_fit)
        leader_pos, leader_fit = whale_pos[ibest], whale_fit[ibest]

        print(leader_pos, leader_fit)

        # converted_pos = apply_along_axis(self.round_position, 1, whale_pos)
        # converted_pos = self.convert_position_in_each_iter(converted_pos)
        # converted_whale_fit = apply_along_axis(self.cost_function, 1, converted_pos)
        # converted_ibest = argmax(converted_whale_fit)
        # converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_whale_fit[
        #     converted_ibest]

        self.iter = 0
        while not self.stopping_criteria(self.iter):
            self.iter += 1
            # self.iter_swarm_pos.loc[self.iter] = converted_pos
            # self.iter_solution.loc[self.iter] = append(converted_leader_pos, converted_leader_fit)

            self.iter_swarm_pos.loc[self.iter] = whale_pos
            self.iter_solution.loc[self.iter] = append(leader_pos, leader_fit)

            if self.debug:
                logger.info("Iteration:{i}/{iterations} - {iter_sol}".format(i=self.iter, iterations=self.iterations,
                                                                             iter_sol=self.iter_solution.loc[
                                                                                 self.iter].to_dict()))
            a = 2 - self.iter * (2 / self.iterations)
            a2 = -1 + self.iter * (-1 / self.iterations)
            whale_pos = asarray([self.update_position(i, whale_pos, leader_pos, a, a2) for i in range(self.population)])

            whale_pos = apply_along_axis(self.boundary_handle, 1, whale_pos)
            whale_fit = apply_along_axis(self.cost_function, 1, whale_pos)

            ibest = argmax(whale_fit)
            if whale_fit[ibest] > leader_fit:
                leader_pos, leader_fit = whale_pos[ibest], whale_fit[ibest]

            # converted_pos = apply_along_axis(self.round_position, 1, whale_pos)
            # converted_pos = self.convert_position_in_each_iter(converted_pos)
            # converted_whale_fit = apply_along_axis(self.cost_function, 1, converted_pos)
            #
            # converted_ibest = argmax(converted_whale_fit)
            # if converted_whale_fit[converted_ibest] > converted_leader_fit:
            #     converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_whale_fit[
            #         converted_ibest]

        self.best_solution.iloc[:] = append(leader_pos, leader_fit)
        return leader_pos, leader_fit

        # self.best_solution.iloc[:] = append(converted_leader_pos, converted_leader_fit)
        # return converted_leader_pos, converted_leader_fit