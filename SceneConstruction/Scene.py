import os
import subprocess
import sys

import pygame

from SceneConstruction.MapMaker import MapMaker
from SceneConstruction.MiniMap import MiniMap
from Config import Config


class Scene:
    def __init__(self):
        pygame.init()
        self.win_surface = pygame.display.set_mode(Config.scene_window_size)
        pygame.display.set_caption("Scene construction")
        self.clock = pygame.time.Clock()
        self.bg_img = pygame.image.load(Config.background_img_path)
        if Config.final_scene_size[0] <= Config.scene_window_size[0]:
            true_window_size = Config.final_scene_size[0]
        else:
            true_window_size = Config.scene_window_size[0]

        self.mini_map = MiniMap(self.win_surface, Config.dividing_line_color, Config.scene_window_size,
                                Config.final_scene_size, Config.show_cell_pixel)
        self.map_maker = MapMaker(Config.scene_window_size[0], true_window_size, Config.rasterized_scene_size,
                                  Config.block_color, Config.default_saved_scene_path, Config.show_cell_pixel)
        self.current_pos = (0, 0)
        self.click_on_mini_map_pos = (0, 0)

        # multi-select mode -> M
        self.multi_select = False
        self.first_select_node = None

        self.show_mini_map_bg = False
        self.mini_map_img = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # handle mouse events
                    click_pos = pygame.mouse.get_pos()
                    if click_pos[1] >= Config.scene_window_size[0]:
                        tmp = click_pos[0]
                        if tmp >= 100:
                            tmp = 100
                        self.click_on_mini_map_pos = (tmp, click_pos[1] - Config.scene_window_size[0])
                    else:
                        self.set_map_val_mouse_button_down(click_pos)
                elif event.type == pygame.KEYDOWN:  # handle keyboard events
                    if event.key == pygame.K_r:
                        self.map_maker.mp.read_map()
                    elif event.key == pygame.K_m:
                        self.multi_select = not self.multi_select
                        self.first_select_node = None
                    elif event.key == pygame.K_s:
                        self.map_maker.mp.write_map()
                        self.show_mini_map_bg = self.map_maker.mp.visualize_map()
                        if sys.platform == "win32":
                            os.startfile(Config.default_saved_scene_img_path)
                        elif sys.platform == "linux":
                            subprocess.call(["xdg-open", Config.default_saved_scene_img_path])
                        elif sys.platform == "darwin":
                            subprocess.call(["open", Config.default_saved_scene_img_path])
            self.win_surface.blit(self.bg_img, (0, 0))
            if self.show_mini_map_bg:
                self.mini_map_img = pygame.image.load(Config.mini_map_img_path)
                self.win_surface.blit(self.mini_map_img, (1, Config.active_window_pixel + 1))
            self.map_maker.draw(self.win_surface, self.current_pos)
            self.current_pos = self.mini_map.update(self.win_surface, self.click_on_mini_map_pos)
            pygame.display.update()
            self.clock.tick(30)

    def set_map_val_mouse_button_down(self, click_position):
        '''
        :param click_position: handle click events  on active window
        '''
        cell_x = int(click_position[0] / Config.show_cell_pixel)
        cell_y = int(click_position[1] / Config.show_cell_pixel)
        pos_x = cell_x + self.current_pos[0]
        pos_y = cell_y + self.current_pos[1]
        if pos_x >= len(self.map_maker.mp.map_data) or pos_y >= len(self.map_maker.mp.map_data[-1]):
            return
        if self.multi_select:  # multi-select for obstacle
            if self.first_select_node is None:
                self.first_select_node = (pos_x, pos_y)
                self.map_maker.mp.map_data[pos_x][pos_y] = 1
                return
            elif self.first_select_node[1] == pos_y or self.first_select_node[0] == pos_x:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    for i in range(self.first_select_node[1], pos_y + 1):
                        for j in range(self.first_select_node[0], pos_x + 1):
                            # print((i, j), end=",")
                            self.map_maker.mp.map_data[j][i] = 1
                    # print("set 1")
                if pygame.mouse.get_pressed() == (0, 0, 1):
                    for i in range(self.first_select_node[1], pos_y + 1):
                        for j in range(self.first_select_node[0], pos_x + 1):
                            # print((i, j), end=",")
                            self.map_maker.mp.map_data[j][i] = 0
                    # print("set 0")
                self.first_select_node = None
            else:
                self.first_select_node = None
        else:
            if pygame.mouse.get_pressed() == (1, 0, 0):  # (1,0,0) means left click
                self.map_maker.mp.map_data[pos_x][pos_y] = 1
            if pygame.mouse.get_pressed() == (0, 0, 1):  # (1,0,0) means right click
                self.map_maker.mp.map_data[pos_x][pos_y] = 0


if __name__ == '__main__':
    scene = Scene()
    scene.run()