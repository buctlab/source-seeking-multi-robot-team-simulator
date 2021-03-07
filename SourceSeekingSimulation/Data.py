import math
import random

import pygame
import pandas as pd

from Config import Config
from SourceSeekingSimulation.spirites.RobotSprite import RobotSprite
from SourceSeekingSimulation.spirites.BlockSprite import BlockSprite
from SourceSeekingSimulation.spirites.PointRobotSprite import PointRobotSprite


class Data:
    def __init__(self, map2d, map2d_detail, cell_size, cell_size_in_real_world, csv_file, number_of_robot):
        self.map2d = map2d
        self.map2d_detail = map2d_detail
        self.cell_size = cell_size
        self.cell_size_in_real_world = cell_size_in_real_world
        self.csv_file_data = []
        self.load_csv_file(csv_file, number_of_robot)

    def load_csv_file(self, csv_file, number_of_robot):
        '''
        load csv file data
        :param csv_file:  csv file path
        :param number_of_robot:  number of robot
        :return:
        '''
        df = pd.read_csv(csv_file)
        count = 0
        tmp = []
        for _, row in df.iterrows():
            if count < number_of_robot:
                tmp.append((
                    int((Config.left_top[0] + row['0']) * (100 / self.cell_size_in_real_world)),
                    int((Config.left_top[1] + row['1']) * (100 / self.cell_size_in_real_world))))
                count += 1
            if count == number_of_robot:
                self.csv_file_data.append(tmp)
                tmp = []
                count = 0

    def load_block(self, group: pygame.sprite.Group, block_color, cell_size, block_img):
        '''
        load obstacle date
        :param group: group to store block
        :param block_color: obstacle color
        :param cell_size: precise in manuscript
        :param block_img: obstacle image path
        '''
        for i in range(len(self.map2d.map_data)):
            for j in range(len(self.map2d.map_data[i])):
                if self.map2d.map_data[i][j] == 1:
                    block = BlockSprite(Config.active_window_pixel, block_color, (i, j), block_img, cell_size,
                                        self.map2d.map_data, )
                    group.add(block)

    def load_robot(self, n, i, group: pygame.sprite.Group, robots):
        '''
        load robot
        :param n: robot number
        :param i: robot id
        :param group: robot group
        :param robots: robot's properties
        :return: RobotSprite instance
        '''
        pos = (self.csv_file_data[0][i][0], self.csv_file_data[0][i][1])
        ag = RobotSprite(i, robots[i]["name"], robots[i]["image"], robots[i]["speed"], robots[i]["size"], pos,
                         self.cell_size, self.map2d_detail)
        group.add(ag)
        return ag

    def load_point_robot(self, ws, group, robot, contour_size):
        '''
        load PointRobotSprite instance
        :param ws: window interface
        :param group: point robot group
        :param robot: robot instance
        :param contour_size: contour size
        :return:
        '''
        pag = PointRobotSprite(ws, robot, contour_size)
        group.add(pag)

    @staticmethod
    def distance(a, b, i, j):
        return (a[i][0] - b[j][0]) * (a[i][0] - b[j][0]) + (a[i][1] - b[j][1]) * (a[i][1] - b[j][1])

    def change_robot_order(self, group, index_a, index_b):
        '''
        swap strategy
        :param group: robot group
        :param index_a: robot index
        :param index_b: robot index
        :return: swap result
        '''
        exist_robot_order = []
        for item in group:
            exist_robot_order.append(item.order)

        result = {}
        if index_b >= len(self.csv_file_data):
            for i in range(len(self.csv_file_data)):
                # if i in exist_robot_order:
                result[i] = i
            return result
        # a = [self.csv_file_data[index_a][i] for i in range(len(exist_robot_order))]
        a = self.csv_file_data[index_a]
        b = self.csv_file_data[index_b]
        if len(exist_robot_order) <= 5:
            a = [self.csv_file_data[index_a][i] for i in range(len(exist_robot_order))]
            b = self.csv_file_data[index_b][:len(exist_robot_order)]
        data = [[0 for _ in range(len(b))] for _ in range(len(a))]
        removed_item_m = {}
        removed_item_n = {}

        for i in range(len(a)):
            for j in range(len(b)):
                data[i][j] = self.distance(a, b, i, j)

        for i in range(len(a)):
            min_dis = 999999
            index_m = -1
            index_n = -1
            for m in range(len(a)):
                for n in range(len(b)):
                    if m in removed_item_m.keys() or n in removed_item_n.keys():
                        continue
                    else:
                        if min_dis > data[m][n]:
                            min_dis = data[m][n]
                            index_m = m
                            index_n = n
            removed_item_m[index_m] = 1
            removed_item_n[index_n] = 1
            if len(exist_robot_order) <= 5:
                result[exist_robot_order[index_m]] = index_n
            else:
                result[index_m] = index_n
        return result