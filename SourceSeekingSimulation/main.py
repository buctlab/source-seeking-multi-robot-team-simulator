import pygame

from SourceSeekingSimulation.MiniMap import MiniMap
from Config import Config
from SourceSeekingSimulation.Map2d import Map2d
from SourceSeekingSimulation.Data import Data
from SourceSeekingSimulation.StateFont import StateFont

pygame.init()
contour_image = pygame.image.load(Config.contour_img_path)

window_surface = pygame.display.set_mode(
    (Config.search_window_size_without_contour[0] + Config.contour_pixel,
     max(Config.search_window_size_without_contour[1], Config.contour_pixel)))

mini_map_img = pygame.image.load(Config.mini_map_img_path)
pygame.display.set_caption("Source seeking simulation")
size = Config.show_cell_pixel
cell_size_in_real_world = Config.rasterized_cell_size
filepath = Config.default_saved_scene_path
csv_file = Config.NIM_data_file_path

bg_img = pygame.image.load(Config.background_img_path)

sf = StateFont(window_surface, Config.func.get_optimum(), Config.leakage_sources)

window_surface.blit(bg_img, (0, 0))
window_surface.blit(contour_image, (Config.search_window_size_without_contour[0] + 1, 0))

block_group = pygame.sprite.Group()
robot_group = pygame.sprite.Group()
point_robot_group = pygame.sprite.Group()
discard_robot_group = pygame.sprite.Group()

map2d = Map2d(filepath)
mini_map = MiniMap(window_surface, Config.dividing_line_color, Config.search_window_size_without_contour,
                   Config.final_scene_size, Config.show_cell_pixel)
map2d_with_robot = Map2d(filepath)

data = Data(map2d, map2d_with_robot, size, cell_size_in_real_world, csv_file, Config.number_of_robots)

data.load_block(block_group, Config.block_color, Config.show_cell_pixel, Config.block_img_path)

clock = pygame.time.Clock()
count = 0

init_pos_count = 0
current_pos = (0, 0)
click_on_mini_map_pos = (0, 0)
interval = 20
interval_count = interval
t = 0

while True:
    pygame.draw.line(window_surface, Config.dividing_line_color,
                     (Config.search_window_size_without_contour[0] - 1, 0),
                     (Config.search_window_size_without_contour[0] - 1,
                      Config.search_window_size_without_contour[0] - 1), 1)
    pygame.draw.line(window_surface, Config.dividing_line_color,
                     (0, Config.search_window_size_without_contour[0] - 1),
                     (Config.search_window_size_without_contour[0] - 1,
                      Config.search_window_size_without_contour[0] - 1), 1)
    pygame.draw.line(window_surface, Config.dividing_line_color,
                     (Config.minimap_size_pixel, Config.search_window_size_without_contour[0] - 1),
                     (Config.minimap_size_pixel,
                      max(Config.search_window_size_without_contour[1], Config.contour_pixel)),
                     1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click event
            click_pos = pygame.mouse.get_pos()
            h_range = (0, Config.minimap_size_pixel)
            v_range = (Config.active_window_pixel, Config.active_window_pixel + Config.minimap_size_pixel)
            if h_range[0] <= click_pos[0] < h_range[1] and \
                    v_range[0] <= click_pos[1] < v_range[1]:
                click_on_mini_map_pos = (click_pos[0], click_pos[1] - Config.active_window_pixel)

    current_pos = mini_map.update(window_surface, click_on_mini_map_pos)

    if interval_count == interval and init_pos_count <= Config.number_of_robots - 1:
        current_robot = data.load_robot(Config.number_of_robots, init_pos_count, robot_group, Config.robots, )
        data.load_point_robot(window_surface, point_robot_group, current_robot, Config.contour_pixel)
        init_pos_count += 1
        interval_count = 0
    else:
        interval_count += 1
    # if init_pos_count <= Config.number_of_robots - 1:  # load robot
    #     current_robot = data.load_robot(Config.number_of_robots, init_pos_count, robot_group, Config.robots,)
    #     data.load_point_robot(window_surface, point_robot_group, current_robot, Config.contour_pixel)
    #     init_pos_count += 1

    if not (False in Config.finished_robots):  # control iteration
        Config.global_iter += 1
        change_dic = data.change_robot_order(robot_group, t, t + 1)
        for robot in robot_group:
            if robot.id in Config.discard_robots:
                Config.finished_robots[robot.id] = True
            else:
                Config.finished_robots[robot.id] = False
                robot.order = change_dic[robot.order]
                robot.finished = False
        t += 1

    block_group.update(current_pos)
    block_group.draw(window_surface)

    robot_group.update(map2d.map_data, data.csv_file_data, robot_group, current_pos)
    robot_group.draw(window_surface)

    point_robot_group.update(robot_group)
    point_robot_group.draw(window_surface)

    if len(robot_group) > 0:
        sf.render_text(robot_group)

    pygame.display.update()
    window_surface.blit(bg_img, (0, 0))
    window_surface.blit(contour_image, (Config.search_window_size_without_contour[0], 0))
    window_surface.blit(mini_map_img, (0, Config.active_window_pixel + 1))
    clock.tick(Config.fps)
