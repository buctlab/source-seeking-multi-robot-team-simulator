import pygame

from SceneConstruction.Map import Map


class MapMaker:
    def __init__(self, scene_window_size, true_window_size, map_in_real_world, block_color, default_file_path, size):
        self.size = size  # active_window_pixel
        self.block_color = block_color  # the color of obstacle
        self.true_window_size = int(true_window_size / self.size)
        self.default_file_path = default_file_path  # Config.default_saved_scene_path
        self.scene_window = int(scene_window_size / self.size)
        self.mp = Map(map_in_real_world[0], map_in_real_world[1], default_file_path)

    def draw(self, ws: pygame.Surface, current_pos):
        '''
        :param ws:
        :param current_pos: pos in manuscript
        :return: None
        '''
        for ty in range(current_pos[1], self.true_window_size + current_pos[1]):
            for tx in range(current_pos[0], self.true_window_size + current_pos[0]):
                if self.mp.map_data[tx][ty] == 1:
                    pygame.draw.rect(ws, self.block_color,
                                     ((tx - current_pos[0]) * self.size + 1, (ty - current_pos[1]) * self.size + 1,
                                      self.size - 2, self.size - 2), 1)
