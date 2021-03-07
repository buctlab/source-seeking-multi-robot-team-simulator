import pygame
from pygame import sprite

from Config import Config
from SourceSeekingSimulation.spirites.RobotSprite import RobotSprite


class PointRobotSprite(sprite.Sprite):
    def __init__(self, window_surface, robot: RobotSprite, contour_size):
        super().__init__()
        self.id = robot.id
        self.contour_size = contour_size
        self.ws = window_surface
        self.image = pygame.image.load(Config.point_robot_img_path)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.get_pos(robot.current_pos[0], robot.current_pos[1])

    def update(self, *args):
        '''
        update point in contour
        :param args: robot_group
        :return: position in contour
        '''
        robot_group = args[0]
        current_robot = None
        for robot in robot_group:
            if robot.id == self.id:
                current_robot = robot
        if current_robot is not None:
            if current_robot is not None:
                if current_robot.discard:
                    self.image = pygame.image.load(Config.discard_robot_img_path)
                    self.rect = self.image.get_rect()
                self.rect.left, self.rect.top = self.get_pos(current_robot.current_pos[0], current_robot.current_pos[1])
        else:
            self.kill()

    def get_pos(self, x, y):
        '''
        transform data to pixel
        :param x:
        :param y: (x, y) means robot position
        :return: pixel in active window
        '''
        tx = x / Config.rasterized_scene_size[0]
        ty = y / Config.rasterized_scene_size[1]
        pix_x = int(tx * self.contour_size) + 1 + Config.active_window_pixel
        pix_y = int(ty * self.contour_size)
        return pix_x, pix_y
