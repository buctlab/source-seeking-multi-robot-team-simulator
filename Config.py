import os

from NIM.benchmarks.multi_source_function import MultiSourceFunction
from NIM.benchmarks.single_source_function import SingleSourceFunction


class Config:
    project_root = os.path.dirname(os.path.realpath(__file__))

    # func = SingleSourceFunction()
    # NIM_data_file_path = os.path.join(project_root, "data/csv_file/ssa_SingleSourceFunction_6.csv")
    # contour_img_path = os.path.join(project_root, "data/bg/contour/SingleSourceFunction.png")
    # leakage_sources = 1
    # iterations = 200

    func = MultiSourceFunction()
    NIM_data_file_path = os.path.join(project_root, "data/csv_file/ssa_MultiSourceFunction_1.csv")
    contour_img_path = os.path.join(project_root, "data/bg/contour/MultiSourceFunction.png")
    leakage_sources = 2
    iterations = 300

    background_img_path = os.path.join(project_root, "data/bg/scene_bg_img.png")
    default_saved_scene_path = os.path.join(project_root, "data/map/default_scene.scene")
    default_saved_scene_img_path = os.path.join(project_root, "data/map/default_scene_img.png")
    mini_map_img_path = os.path.join(project_root, "data/bg/mini_map_img.png")
    point_robot_img_path = os.path.join(project_root, "data/robot/point_robot.png")
    discard_robot_img_path = os.path.join(project_root, "data/robot/discard_point_robot.png")
    block_img_path = os.path.join(project_root, "data/block/block_img.png")
    source_tag_img_path = os.path.join(project_root, "data/bg/source_tag_img.png")

    exist_zero = 1
    scene_size = (
        func.upper[1] - func.lower[1] + 1 * exist_zero, func.upper[1] - func.lower[1] + 1 * exist_zero)  # m

    rasterized_cell_size = 10  # cm

    # size of map array
    entrance = (195, 200)
    rasterized_scene_size = (
        int((scene_size[0] - 1 * exist_zero) * 100 / rasterized_cell_size) + 1 * exist_zero,
        int((scene_size[1] - 1 * exist_zero) * 100 / rasterized_cell_size) + 1 * exist_zero)

    show_cell_pixel = 10

    left_top = (abs(func.lower[0]), abs(func.lower[1]))

    final_scene_size = (
        int((scene_size[0] - 1 * exist_zero) * 100 / rasterized_cell_size * show_cell_pixel) + 1 * exist_zero,
        int((scene_size[1] - 1 * exist_zero) * 100 / rasterized_cell_size * show_cell_pixel) + 1 * exist_zero)

    minimap_size_pixel = 100
    active_window_pixel = 500
    search_window_size_without_contour = (
        active_window_pixel + 1, active_window_pixel + minimap_size_pixel + 1)
    scene_window_size = (active_window_pixel, active_window_pixel + minimap_size_pixel + 1)

    contour_pixel = 500

    block_color = (0, 0, 0)
    dividing_line_color = (0, 0, 0)

    fps = 80

    robots = [
        {"name": "No.0 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi0.png"), "speed": 1,
         "priority": 3, "size": (1, 1)},
        {"name": "No.1 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi1.png"), "speed": 1,
         "priority": 2, "size": (1.5, 1)},
        {"name": "No.2 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi2.png"), "speed": 2,
         "priority": 3, "size": (1, 1.5)},
        {"name": "No.3 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi3.png"), "speed": 1,
         "priority": 1, "size": (1.5, 1.5)},
        {"name": "No.4 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi4.png"), "speed": 2,
         "priority": 1, "size": (1, 1)},
        {"name": "No.5 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi5.png"), "speed": 1,
         "priority": 2, "size": (1, 1)},
        {"name": "No.6 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi6.png"), "speed": 1,
         "priority": 1, "size": (2, 1)},
        {"name": "No.7 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi7.png"), "speed": 5,
         "priority": 5, "size": (1, 1)},
        {"name": "No.8 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi8.png"), "speed": 1,
         "priority": 5, "size": (1, 1)},
        {"name": "No.9 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi9.png"), "speed": 1,
         "priority": 3, "size": (1, 1)},
        {"name": "No.10 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi10.png"), "speed": 1,
         "priority": 8, "size": (1.5, 1.5)},
        {"name": "No.11 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi11.png"), "speed": 2,
         "priority": 5, "size": (1, 1)},
        {"name": "No.12 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi12.png"), "speed": 1,
         "priority": 9, "size": (1, 1)},
        {"name": "No.13 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi13.png"), "speed": 4,
         "priority": 10, "size": (1.5, 1)},
        {"name": "No.14 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi14.png"), "speed": 1,
         "priority": 6, "size": (1, 1)},
        {"name": "No.15 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi15.png"), "speed": 3,
         "priority": 7, "size": (1, 1.5)},
        {"name": "No.16 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi16.png"), "speed": 1,
         "priority": 10, "size": (1, 1)},
        {"name": "No.17 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi17.png"), "speed": 3,
         "priority": 10, "size": (1, 1)},
        {"name": "No.18 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi18.png"), "speed": 1,
         "priority": 8, "size": (1, 1)},
        {"name": "No.19 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi19.png"), "speed": 2,
         "priority": 4, "size": (1, 1)},
    ]

    # robots = [
    #     {"name": "No.0 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi0.png"), "speed": 1,
    #      "priority": 3, "size": (0.5, 0.5)},
    #     {"name": "No.1 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi1.png"), "speed": 1,
    #      "priority": 2, "size": (1, 1)},
    #     {"name": "No.2 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi2.png"), "speed": 2,
    #      "priority": 3, "size": (0.5, 1)},
    #     {"name": "No.3 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi3.png"), "speed": 1,
    #      "priority": 1, "size": (0.5, 0.5)},
    #     {"name": "No.4 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi4.png"), "speed": 2,
    #      "priority": 1, "size": (0.5, 0.5)},
    #     {"name": "No.5 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi5.png"), "speed": 1,
    #      "priority": 2, "size": (1, 1)},
    #     {"name": "No.6 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi6.png"), "speed": 1,
    #      "priority": 1, "size": (0.5, 0.5)},
    #     {"name": "No.7 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi7.png"), "speed": 5,
    #      "priority": 5, "size": (1, 1.5)},
    #     {"name": "No.8 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi8.png"), "speed": 1,
    #      "priority": 5, "size": (0.5, 0.5)},
    #     {"name": "No.9 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi9.png"), "speed": 1,
    #      "priority": 3, "size": (0.5, 0.5)},
    #     {"name": "No.10 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi10.png"), "speed": 1,
    #      "priority": 8, "size": (0.5, 0.5)},
    #     {"name": "No.11 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi11.png"), "speed": 2,
    #      "priority": 5, "size": (1, 1)},
    #     {"name": "No.12 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi12.png"), "speed": 1,
    #      "priority": 9, "size": (1, 1)},
    #     {"name": "No.13 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi13.png"), "speed": 4,
    #      "priority": 10, "size": (0.5, 1)},
    #     {"name": "No.14 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi14.png"), "speed": 1,
    #      "priority": 6, "size": (1, 1)},
    #     {"name": "No.15 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi15.png"), "speed": 3,
    #      "priority": 7, "size": (1, 1.5)},
    #     {"name": "No.16 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi16.png"), "speed": 1,
    #      "priority": 10, "size": (1, 1)},
    #     {"name": "No.17 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi17.png"), "speed": 3,
    #      "priority": 10, "size": (1, 1)},
    #     {"name": "No.18 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi18.png"), "speed": 1,
    #      "priority": 8, "size": (0.5, 0.5)},
    #     {"name": "No.19 robot", "image": os.path.join(project_root, "data/robot/robots_img/shuzi19.png"), "speed": 2,
    #      "priority": 4, "size": (1, 1)},
    # ]

    size = list(map(lambda x: x["size"], robots))
    robots = sorted(robots, key=lambda rt: (rt["priority"], rt["speed"]), reverse=True)

    global_iter = 0
    number_of_robots = len(robots)
    discard_robots = []
    finished_robots = [False for _ in range(number_of_robots)]
