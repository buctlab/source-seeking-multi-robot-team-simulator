import pygame

from Config import Config


class MiniMap:
    def __init__(self, win_surface, dividing_line_color, scene_window_size, scene_size, cell_size):
        self.dividing_line_color = dividing_line_color  # dividing_line color between mini-map and active window
        self.scene_window_size = scene_window_size  # pygame window size
        self.scene_size = scene_size  # scene data after rasterization
        self.cell_size = cell_size  # precision in manuscript
        self.mini_map_size = Config.minimap_size_pixel
        self.scene_window_height_or_width = int(self.scene_window_size[0] / self.cell_size)
        self.scene_height = int(self.scene_size[-1] / self.cell_size)
        self.scene_width = int(self.scene_size[0] / self.cell_size)
        self.mini_window_size_h = int(self.scene_window_height_or_width / self.scene_width * self.mini_map_size)
        self.mini_window_size_v = int(self.scene_window_height_or_width / self.scene_height * self.mini_map_size)
        # draw red rectangle in mini-map
        pygame.draw.rect(win_surface, [255, 0, 0],
                         (0, self.scene_window_size[0] + 1, self.mini_window_size_h, self.mini_window_size_v), width=1)

    def draw_line(self, win_surface):
        pygame.draw.line(win_surface, self.dividing_line_color, (0, self.scene_window_size[0] + 1),
                         (self.scene_window_size[0] + 1, self.scene_window_size[0] + 1), 1)
        pygame.draw.line(win_surface, self.dividing_line_color,
                         (self.scene_window_size[1] - self.scene_window_size[0], self.scene_window_size[0] + 1),
                         (self.scene_window_size[1] - self.scene_window_size[0], self.scene_window_size[1]), 1)

    def draw_mini_map(self, win_surface, click_pos):
        '''
        draw red rectangle in mini-map
        :param win_surface: pygame window surface
        :param click_pos: click position on mini-map
        :return: 'pos' in in manuscript
        '''
        ta = 0
        tb = 0
        click_pos_h = click_pos[0]
        click_pos_v = click_pos[1]
        draw_pos_h = 0
        draw_pos_v = 0
        if click_pos_h - int(self.mini_window_size_h / 2) > 0:
            draw_pos_h = click_pos_h - int(self.mini_window_size_h / 2)
        if click_pos_v - int(self.mini_window_size_v / 2) > 0:
            draw_pos_v = click_pos_v - int(self.mini_window_size_v / 2)
        if click_pos_h + int(self.mini_window_size_h / 2) >= self.mini_map_size:
            draw_pos_h = max(0, self.mini_map_size - self.mini_window_size_h)
            ta = 1
        if click_pos_v + int(self.mini_window_size_v / 2) >= self.mini_map_size:
            draw_pos_v = max(self.mini_map_size - self.mini_window_size_v, 0)
            tb = 1

        pygame.draw.rect(win_surface, [255, 0, 0],
                         (draw_pos_h, draw_pos_v + self.scene_window_size[0] + 1,
                          min(self.mini_window_size_h, self.mini_map_size),
                          min(self.mini_window_size_v, self.mini_map_size)), width=1)
        t1 = int(draw_pos_h / self.mini_map_size * self.scene_width)
        t2 = int(draw_pos_v / self.mini_map_size * self.scene_height)
        if ta == 1:
            t1 += 1
        if tb == 1:
            t2 += 1
        return t1, t2

    def update(self, win_surface, click_pos):
        '''
        update interface in each frame including red rectangle and dividing line
        :param win_surface: pygame window surface
        :param click_pos: 'click position on mini-map
        :return: 'pos' in in manuscript
        '''
        self.draw_line(win_surface)
        pos = self.draw_mini_map(win_surface, click_pos)
        return pos
