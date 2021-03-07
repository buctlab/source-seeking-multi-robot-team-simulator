import imageio
import numpy as np
from PIL import Image

from Config import Config


class Map:

    def __init__(self, w, h, default_file_path):
        self.w = w  # Scene width
        self.h = h  # Scene height
        self.default_file_path = default_file_path  # Config.default_saved_scene_path
        self.map_data = [[0 for _ in range(h)] for _ in range(w)]  # Scene data

    def show_map_data(self):
        for i in range(self.h):
            for j in range(self.w):
                print(self.map_data[i][j], end=" ")
            print("")

    def visualize_map(self):
        '''
        visualize scene data
        :return: return whether the conversion from data to image is successful
        '''
        data = [[0 for _ in range(self.w)] for _ in range(self.h)]
        for i in range(self.w):
            for j in range(self.h):
                if self.map_data[j][i] == 1:
                    data[i][j] = 0
                if self.map_data[j][i] == 0:
                    data[i][j] = 1
        try:
            imageio.imwrite(Config.default_saved_scene_img_path, np.asarray(data))
            mini_map_bg = Image.open(Config.default_saved_scene_img_path)
            mini_map_bg = mini_map_bg.resize((Config.minimap_size_pixel, Config.minimap_size_pixel), Image.ANTIALIAS)
            mini_map_bg.save(Config.mini_map_img_path)
            return True
        except Exception as e:
            print(e)
            return False

    # sava scene data
    def write_map(self):
        with open(self.default_file_path, mode="w") as f:
            f.write(str(self.map_data))

    # read map data
    def read_map(self):
        with open(self.default_file_path, 'r') as f:
            data = f.read()
        self.map_data = eval(data)
