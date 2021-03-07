import copy
from random import random

import pygame

from SourceSeekingSimulation.AstarSearch import AstarSearch
from Config import Config


class RobotSprite(pygame.sprite.Sprite):
    def __init__(self, i, name, path, speed, size, rect_pos, cell_size, map2d_detail, preset_trigger=5):
        super().__init__()
        self.speed = speed
        self.name = name
        self.id = i
        self.img_path = path
        self.cell_size = cell_size
        self.order = i
        self.path = []  # store path data
        self.step = 0  # record index in path
        self.finished = False  # control iteration in each generation
        self.wd_size = Config.active_window_pixel / Config.show_cell_pixel
        self.size = int(size[0] * 2), int(size[1] * 2)
        self.entrance = (Config.entrance[0], int(Config.entrance[1] - self.size[0]))
        self.image = pygame.transform.scale(pygame.image.load(self.img_path), (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect()
        self.current_pos = self.entrance  # entrance
        self.draw_robot_in_active_window((0, 0))

        # when there is no movement for 'still_count' times,
        # the intra-generation swap strategy and the local path search are triggered
        self.preset_trigger = preset_trigger

        self.end_position = rect_pos  # the end position in each pathfinding

        self.no_movement_count = 0
        self.preset_no_movement = 5

        self.no_path_count = 0
        self.preset_no_path = 5

        self.discard = False
        self.preset_discard = 2
        self.intra_generation_swap_count = 0  # times of  swap strategy
        self.local_path_search_count = 0  # times of local path search
        # when intra_generation_swap_count or local_path_search_count reaches preset_discard, discard it

        self.current_pos = self.entrance  # entrance

        self.change_list = []

        self.map2d_detail = map2d_detail  # scene data for local path search
        self.map2d_detail.set_map2d_value(self.current_pos[0], self.current_pos[1], 1)

        # self.draw_robot_in_active_window(self.current_pos)

    def draw_robot_in_active_window(self, pos, keep=False):
        '''
        draw robot in active window
        :param pos: pos in manuscript
        :param keep: whether is still
        '''
        if pos[0] <= self.current_pos[0] < pos[0] + self.wd_size and \
                pos[1] <= self.current_pos[1] < pos[1] + self.wd_size:
            if self.finished or keep:
                self.rect.left, self.rect.top = (self.current_pos[0] - pos[0]) * self.cell_size, \
                                                (self.current_pos[1] - pos[1]) * self.cell_size
            else:
                self.rect.left, self.rect.top = (self.path[self.step][0] - pos[0]) * self.cell_size, \
                                                (self.path[self.step][1] - pos[1]) * self.cell_size
        else:
            self.rect.left, self.rect.top = -200, -200

    def check_occupation(self, use_map, h, w):
        '''
        :param use_map: scene data
        :param h:
        :param w: current position (h,w)
        :return: whether is occupied
        '''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if 0 <= h + j < len(use_map) and 0 <= w + i < len(use_map[-1]) and use_map[h + j][w + i] == 1:
                    return False
        return True


    def position_correction(self, use_map, h, w):
        '''
        :param use_map: scene data
        :param h:
        :param w: current position (h,w)
        :return: available end point
        '''
        w_min = max(0, w - self.size[0] + 1)
        h_min = max(0, h - self.size[1] + 1)
        available_position = []
        for i in range(h_min, h + 1):
            for j in range(w_min, w + 1):
                if self.check_occupation(use_map, i, j):
                    available_position.append((i, j))
        return available_position

    def contain_end_position(self, h, w):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.end_position[0] == h + j and self.end_position[1] == w + i:
                    return True

    # check to reach the end position
    def arrived_current_end_position(self):
        h, w = self.current_pos
        return self.current_pos == self.end_position or self.contain_end_position(h, w)

    def set_robot_occupation(self, p0, p1, value):
        '''
        :param p0:
        :param p1: current_pos(p0,p1)
        :param value: 1 or 0
        :return:
        '''
        a, b = self.size
        for i in range(a):
            for j in range(b):
                self.map2d_detail.set_map2d_value(p0 + i, p1 + j, value)

    def calculate_path(self, use_map):
        '''
        use A* to calculate path
        :param use_map: scene data
        :param ignore: ignore position
        :return: path
        '''
        if isinstance(use_map, list):
            copy_map = copy.deepcopy(use_map)
        else:
            copy_map = copy.deepcopy(use_map.map_data)
        a, b = self.size
        for i in range(a):
            for j in range(b):
                copy_map[self.current_pos[0] + i][self.current_pos[1] + j] = 0
        eps = self.position_correction(copy_map, self.end_position[0], self.end_position[1])
        self.step = 0
        for item in eps:
            self.path = AstarSearch().get_path(copy_map, (self.current_pos[0], self.current_pos[1]), item, a, b)
            if self.path:
                return
        return

    def discard_strategy(self, robot_group):
        if self.discard:
            robot_group.remove(self)
            Config.discard_robots.append(self.id)
            Config.finished_robots[self.id] = True
            print(self.id, "robot removes")
            print(self.path)
            print(self.end_position)

        self.discard = True
        print(self.id, "robot discards")
        self.end_position = self.entrance

    def is_colliding(self, robot_groups, next_pos):
        '''
        check colliding
        :param robot_groups: robot group
        :param next_pos: next position in path
        :return: colliding or not
        '''
        for robot in robot_groups:
            if self == robot:
                continue
            else:
                if next_pos in robot.current_pos:
                    return True, self, robot
        return False, -1, -1

    def intra_generation_strategy(self, coa, cob):
        coa.order, cob.order = cob.order, coa.order
        self.path = []
        self.step = 0

    # update position in each frame
    def update(self, *args, **kwargs):

        map2d = args[0]  # scene data for global path search
        csv_data = args[1]  # position of all generation (for intra-generation swap)
        robot_group = args[2]
        pos = args[3]

        # reach current destination in each generation
        if self.arrived_current_end_position():
            # discard and reach entrance
            if self.discard:
                print(self.id, "robot reached entrance, discard")
                robot_group.remove(self)
                Config.discard_robots.append(self.id)
                Config.finished_robots[self.id] = True
            else:
                # reach max iteration, keep
                if Config.global_iter >= len(csv_data):
                    print(self.id, "robot reaches max iteration")
                    self.draw_robot_in_active_window(pos, True)
                    return
                else:
                    current_end_position = self.end_position
                    # reach current iteration, waiting for other robots
                    if current_end_position == csv_data[Config.global_iter][self.order]:
                        print(self.id, "robot reaches current iteration, waiting for other robots")
                        self.finished = True
                        Config.finished_robots[self.id] = True
                        self.draw_robot_in_active_window(pos, True)
                        return
                    # global iteration increased, set next end position
                    else:
                        print("global iteration increased", self.id, "robot sets next end position")
                        self.end_position = csv_data[Config.global_iter][self.order]
                        self.finished = False
                        Config.finished_robots[self.id] = False
                        self.path = []
                        self.step = 0
                        self.draw_robot_in_active_window(pos, True)
                        return
        else:
            # no path -> pathfinding
            if not self.path or self.no_movement_count >= self.preset_no_movement:
                print(self.id, "pathfinding")
                if self.no_path_count >= self.preset_no_path or self.no_movement_count > self.preset_no_movement and \
                        self.intra_generation_swap_count + self.local_path_search_count > self.preset_discard:
                    print(self.id, "discard strategy")
                    self.discard_strategy(robot_group)
                    self.no_path_count = 0
                    self.draw_robot_in_active_window(pos, True)
                    return
                if self.local_path_search_count > 0:
                    print(self.id, "local path search count")
                    print(self.id, "path:", self.path)
                    self.calculate_path(self.map2d_detail)
                else:
                    print(self.id, "local path search")
                    self.calculate_path(map2d)
                if not self.finished and self.path == []:
                    print(self.id, "local path search count + 1")
                    self.no_path_count += 1
                    self.draw_robot_in_active_window(pos, True)
                    return
                else:
                    print(self.id, "local path search count reset")
                    self.no_path_count = 0
                    self.no_movement_count = 0
            # ready to move
            else:
                print(self.id, "ready to move")
                previous_step = self.step
                self.step += 1
                if self.step >= len(self.path):
                    self.draw_robot_in_active_window(pos)
                    print(self.id, "out of path")
                    return
                colliding, coa, cob = self.is_colliding(robot_group, (self.path[self.step][0], self.path[self.step][1]))
                # colliding at the beginning
                if colliding:
                    print(self.id, "colliding", cob.id)
                    self.no_movement_count += 1
                    self.step = previous_step
                    self.draw_robot_in_active_window(pos, keep=True)
                    if self.no_movement_count >= self.preset_no_movement:
                        if Config.finished_robots[cob.id] or self.intra_generation_swap_count > 0:
                            self.local_path_search_count += 1
                            self.draw_robot_in_active_window(pos, True)
                            return
                        else:
                            self.intra_generation_strategy(coa, cob)
                            self.intra_generation_swap_count += 1
                            self.draw_robot_in_active_window(pos, True)
                            return
                else:
                    print(self.id, "move")
                    self.intra_generation_swap_count = 0
                    self.no_movement_count = 0
                    self.local_path_search_count = 0
                    actual_speed = min(len(self.path[self.step:]), self.speed)

                    moved_pos = (self.path[self.step][0], self.path[self.step][1])
                    actual_step = 0
                    for i in range(1, actual_speed):
                        colliding, coa, cob = self.is_colliding(robot_group,
                                                                (self.path[self.step + i][0],
                                                                 self.path[self.step + i][1]))
                        if colliding:
                            break
                        else:
                            actual_step = i
                            moved_pos = (self.path[self.step + i][0], self.path[self.step + i][1])

                    self.set_robot_occupation(self.current_pos[0], self.current_pos[1], 0)
                    self.set_robot_occupation(moved_pos[0], moved_pos[1], 1)
                    self.current_pos = moved_pos
                    self.step = self.step + actual_step
                    self.draw_robot_in_active_window(pos)
