import pygame

from Config import Config


class MiniMap:
    def __init__(self, win_surface, dividing_line_color, scene_window_size, scene_size, cell_size):
        self.dividing_line_color = dividing_line_color
        self.scene_window_size = scene_window_size
        self.scene_size = scene_size
        self.cell_size = cell_size
        self.mini_map_size = Config.minimap_size_pixel
        self.scene_window_height_or_width = int(Config.active_window_pixel / self.cell_size)
        self.scene_height = int(self.scene_size[-1] / self.cell_size)
        self.scene_width = int(self.scene_size[0] / self.cell_size)
        self.mini_window_size_h = int(self.scene_window_height_or_width / self.scene_width * self.mini_map_size)
        self.mini_window_size_v = int(self.scene_window_height_or_width / self.scene_height * self.mini_map_size)
        self.source_tag_img = pygame.image.load(Config.source_tag_img_path)
        self.opt_position = []
        self.calculate4position()
        pygame.draw.rect(win_surface, [255, 0, 0],
                         (0, self.scene_window_size[0] - 1, self.mini_window_size_h, self.mini_window_size_v), width=1)

    def draw_mini_map(self, win_surface, click_pos):
        click_pos_h = click_pos[0]
        click_pos_v = click_pos[1]
        draw_pos_h = 0
        draw_pos_v = 0
        ta = 0
        tb = 0
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
                         (draw_pos_h, draw_pos_v + Config.active_window_pixel,
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
        self.show_source_in_mini_map(win_surface)
        return self.draw_mini_map(win_surface, click_pos)

    def calculate4position(self):
        size = self.source_tag_img.get_size()
        opt, _ = Config.func.get_optimum()
        for each_opt in opt:
            tx = int(Config.minimap_size_pixel * (each_opt[0] - Config.func.lower[0]) / (
                    Config.func.upper[0] - Config.func.lower[0]))
            ty = int(Config.minimap_size_pixel * (each_opt[1] - Config.func.lower[1]) / (
                    Config.func.upper[1] - Config.func.lower[1]))
            self.opt_position.append((tx - size[0] / 2, ty - size[1] / 2))

    def show_source_in_mini_map(self, win_surface):
        for item in self.opt_position:
            win_surface.blit(self.source_tag_img, (item[0], item[1] + 1 + Config.active_window_pixel))
