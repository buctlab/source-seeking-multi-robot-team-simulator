from NIM.algorithms.algorithm import Algorithm, Ackley
from numpy import asarray, zeros, inf, apply_along_axis, where, exp, argmin, append, sqrt, argmax
import logging
import pandas as pd

logging.basicConfig()
logger = logging.getLogger('SSA')
logger.setLevel('INFO')


class SalpSwarmAlgorithm(Algorithm):

    def __init__(self, map2d, cell_size, **kwargs):
        super().__init__(map2d, cell_size, **kwargs)

    def update_position(self, i, c1, salp_pos, food_pos):
        '''
        update next generation
        :param i: index
        :param c1: parameter in algo
        :param salp_pos: salp position in previous generation
        :param food_pos: best position in previous generation
        :return: next generation
        '''
        new_salp_pos = zeros(self.dim)
        if i <= self.population / 2:
            c2 = self.Rand.uniform(self.lower, self.upper, self.dim)
            c3 = self.Rand.rand(self.dim)
            index_l, index_g = where(c3 < 0.5), where(c3 >= 0.5)
            new_salp_pos[index_l] = food_pos[index_l] + c1 * c2[index_l]
            new_salp_pos[index_g] = food_pos[index_g] - c1 * c2[index_g]
        elif i < self.population:
            new_salp_pos = (salp_pos[i - 1] + salp_pos[i]) / 2
        return new_salp_pos

    def construct_new_salp(self, result, c1):
        '''
        calculate new position
        :param result: clustering result
        :param c1: parameter in algo
        :return: new salp position, new salp fit, new salp cluster
        '''
        new_salp = []
        new_salp_cluster = []
        new_salp_fit = []
        for name, group in result.groupby('c'):
            leader_pos = group['f'].idxmax()
            for i in range(len(group)):
                salp = self.update_position(i, c1, result.iloc[:, 2:].values, result.iloc[leader_pos, 2:].values)
                salp = self.boundary_handle(asarray(salp))
                new_salp.append(salp)
                new_salp_cluster.append(name)
                new_salp_fit.append(self.cost_function(salp))
        new_salp_cluster = pd.DataFrame(new_salp_cluster, columns=['c'])  # 根据c列索引创建dataframe
        new_salp_fit = pd.DataFrame(new_salp_fit, columns=['f'])
        new_salp = pd.DataFrame(new_salp)
        return new_salp, new_salp_fit, new_salp_cluster

    def update_solutions(self, new_salp, new_salp_fit, new_salp_cluster, salp_pos, salp_fit, salp_cluster):
        '''
        replace current position with closest position in new_salp if it is better fitness
        :param new_salp: new salp position from construct_new_salp()
        :param new_salp_fit: new salp fit from construct_new_salp()
        :param new_salp_cluster:  new salp cluster from construct_new_salp()
        :param salp_pos: current salp position
        :param salp_fit: current salp fit
        :param salp_cluster: current salp cluster
        :return: next generation
        '''
        for i, row in new_salp.iterrows():
            distance_vector = []
            for j, r in salp_pos.iterrows():
                distance_vector.append(sqrt((((row - r) ** 2).values).sum()))
            nearest_whale = distance_vector.index(min(distance_vector))
            if new_salp_fit.iloc[i]['f'] > salp_fit.iloc[nearest_whale]['f']:
                salp_fit.iloc[nearest_whale] = new_salp_fit.iloc[i]
                salp_pos.iloc[nearest_whale] = row
                salp_cluster.iloc[nearest_whale] = new_salp_cluster.iloc[i]
        result = pd.concat([salp_cluster, salp_fit, salp_pos], axis=1)  # 将三个数据垂直方向进行拼接
        return result

    # locating the single source
    def run_single_source(self):
        salp_pos = self.initial_position()
        salp_fit = apply_along_axis(self.cost_function, 1, salp_pos)
        self.iter = 0

        ibest = argmax(salp_fit)
        food_pos, food_fit = salp_pos[ibest], salp_fit[ibest]

        converted_pos = apply_along_axis(self.round_position, 1, salp_pos)
        converted_pos = self.convert_position_in_each_iter(converted_pos)
        converted_food_fit = apply_along_axis(self.cost_function, 1, converted_pos)
        converted_ibest = argmax(converted_food_fit)
        converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_food_fit[
            converted_ibest]

        while not self.stopping_criteria(self.iter):
            self.iter += 1
            self.iter_swarm_pos.loc[self.iter] = converted_pos
            self.iter_solution.loc[self.iter] = append(converted_leader_pos, converted_leader_fit)
            if self.debug:
                logger.info("Iteration:{i}/{iterations} - {iter_sol}".format(i=self.iter, iterations=self.iterations,
                                                                             iter_sol=self.iter_solution.loc[
                                                                                 self.iter].to_dict()))
            c1 = 2 * exp(-(4 * self.iter / self.iterations) ** 2)
            salp_pos = asarray([self.update_position(i, c1, salp_pos, food_pos) for i in range(self.population)])
            salp_pos = apply_along_axis(self.boundary_handle, 1, salp_pos)
            salp_fit = apply_along_axis(self.cost_function, 1, salp_pos)

            ibest = argmax(salp_fit)
            if salp_fit[ibest] > food_fit:
                food_pos, food_fit = salp_pos[ibest], salp_fit[ibest]

            converted_pos = apply_along_axis(self.round_position, 1, salp_pos)
            converted_pos = self.convert_position_in_each_iter(converted_pos)
            converted_food_fit = apply_along_axis(self.cost_function, 1, converted_pos)

            converted_ibest = argmax(converted_food_fit)
            if converted_food_fit[converted_ibest] > converted_leader_fit:
                converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_food_fit[
                    converted_ibest]
        self.best_solution.iloc[:] = append(converted_leader_pos, converted_leader_fit)
        return converted_leader_pos, converted_leader_fit

    # locating the multi-source
    def run_multi_source(self):
        salp_pos = pd.DataFrame(self.initial_position())
        salp_fit = salp_pos.apply(self.cost_function, axis=1).astype('float')
        self.iter = 0

        ibest = argmax(salp_fit.values)
        food_pos, food_fit = salp_pos.values[ibest], salp_fit.values[ibest]

        converted_pos = apply_along_axis(self.round_position, 1, salp_pos.values)
        converted_pos = self.convert_position_in_each_iter(converted_pos)
        converted_food_fit = apply_along_axis(self.cost_function, 1, converted_pos)
        converted_ibest = argmax(converted_food_fit)
        converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_food_fit[
            converted_ibest]

        while not self.stopping_criteria(self.iter):
            self.iter += 1
            self.iter_swarm_pos.loc[self.iter] = converted_pos
            self.iter_solution.loc[self.iter] = append(converted_leader_pos, converted_leader_fit)

            if self.debug:
                logger.info("Iteration:{i}/{iterations} - {iter_sol}".format(i=self.iter, iterations=self.iterations,
                                                                             iter_sol=self.iter_solution.loc[
                                                                                 self.iter].to_dict()))
                c1 = 2 * exp(-(4 * self.iter / self.iterations) ** 2)

                salp_cluster, salp_fit, salp_pos, result = self.kmeans(self.k, salp_pos, salp_fit)
                new_salp, new_salp_fit, new_salp_cluster = self.construct_new_salp(result, c1)
                result = self.update_solutions(new_salp, new_salp_fit, new_salp_cluster, salp_pos, salp_fit,
                                               salp_cluster)

                salp = result.iloc[:, 2:].values
                salp = apply_along_axis(self.round_position, 1, salp)
                salp = apply_along_axis(self.boundary_handle, 1, salp)

                converted_pos = self.convert_position_in_each_iter(salp)
                converted_food_fit = apply_along_axis(self.cost_function, 1, converted_pos)

                salp_pos = pd.DataFrame(salp)
                salp_fit = salp_pos.apply(self.cost_function, axis=1).astype('float')

                # print(salp_pos, salp_fit)

                ibest = argmax(salp_fit.values)
                if salp_fit.values[ibest] >= food_fit:
                    food_pos, food_fit = salp_pos.values[ibest], salp_fit.values[ibest]

                salp_pos = salp_pos.values

            converted_ibest = argmax(converted_food_fit)
            if converted_food_fit[converted_ibest] > converted_leader_fit:
                converted_leader_pos, converted_leader_fit = converted_pos[converted_ibest], converted_food_fit[
                    converted_ibest]

        self.best_solution.iloc[:] = append(converted_leader_pos, converted_leader_fit)
        return converted_leader_pos, converted_leader_fit

    def run(self):
        '''
        select different function according to k
        :return: source position
        '''
        if self.k == 1:
            return self.run_single_source()
        else:
            return self.run_multi_source()
