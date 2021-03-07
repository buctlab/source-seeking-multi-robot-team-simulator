import pygame
import math
from Config import Config


class StateFont:
    def __init__(self, window_surface, global_best, k, font="freesansbold.ttf", current_pos=(150, 505),
                 best_pos=(150, 530), value_pos=(150, 555), iter_pos=(150, 580)):
        self.window_surface = window_surface
        self.font = pygame.font.SysFont(font, 30)

        self.global_best, _ = global_best
        self.k = k

        self.current_pos = current_pos
        self.best_pos = best_pos
        self.value_pos = value_pos
        self.iter_pos = iter_pos

    def render_text(self, robots):
        '''
        render text in interface
        :param robots: robot group
        '''
        current_robot, value = self.calculate(robots)
        if current_robot is None:
            rt1 = f"Current best: "
        else:
            rt1 = f"Current best: {', '.join(i.name for i in current_robot)}"
        rt2 = f"Global best: {', '.join(str(i) for i in self.global_best)}"

        current_robot, value = self.calculate(robots)
        if current_robot is None:
            rt3 = f"Distance: "
        else:
            rt3 = f"Distance: {', '.join(str(round(i, 4)) for i in value)}"

        rt4 = f"Iteration: {Config.global_iter}"
        self.window_surface.blit(self.font.render(rt1, True, (0, 0, 0)), self.current_pos)
        self.window_surface.blit(self.font.render(rt2, True, (0, 0, 0)), self.best_pos)
        self.window_surface.blit(self.font.render(rt3, True, (0, 0, 0)), self.value_pos)
        self.window_surface.blit(self.font.render(rt4, True, (0, 0, 0)), self.iter_pos)

    def calculate(self, robots):
        '''
        calculate min distance to each source
        :param robots: robot group
        :return: min distance to each source
        '''
        min_robot = []
        min_distance = []

        distance_data = [[] for _ in range(len(self.global_best))]

        robots_list = []

        for ag in robots:
            if ag.discard:
                continue
            tmp = self.distance(ag)
            robots_list.append(ag)
            for i in range(len(self.global_best)):
                distance_data[i].append(tmp[i])

        tt = 0
        for dd in distance_data:
            if not dd:
               tt += 1
        if tt == len(distance_data):
            return None, None


        for i in range(len(distance_data)):
            min_value = min(distance_data[i])
            min_index = distance_data[i].index(min_value)
            min_robot.append(robots_list[min_index])
            min_distance.append(min_value)
        return min_robot, min_distance

    def distance(self, ag):
        '''
        calculate distance
        :param ag: robot group
        :return: distance from source
        '''
        distance_from_source = []
        pos = ag.current_pos
        size = [int(Config.size[ag.id][0] * 2), int(Config.size[ag.id][1] * 2)]
        p0 = pos[0] * Config.rasterized_cell_size / 100 + Config.func.lower[0]
        p1 = pos[1] * Config.rasterized_cell_size / 100 + Config.func.lower[1]
        for item in self.global_best:
            t = 999999
            for v in range(size[0]):
                for h in range(size[1]):
                    d = abs(p0 + Config.rasterized_cell_size * h / 100 - item[0]) + abs(
                        p1 + Config.rasterized_cell_size * v / 100 - item[1])
                    if t > d:
                        t = d
            distance_from_source.append(t)
        return distance_from_source
