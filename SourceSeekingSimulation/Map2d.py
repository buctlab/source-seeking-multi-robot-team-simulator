class Map2d:
    def __init__(self, default_file_path):
        self.map_data = None
        self.h = None
        self.w = None
        self.set_map2d(default_file_path)

    def set_map2d(self, default_file_path):
        with open(default_file_path, 'r') as f:
            data = f.read()
        self.map_data = eval(data)
        self.h = len(self.map_data)
        self.w = len(self.map_data[-1])

    def set_map2d_value(self, x, y, value):
        self.map_data[x][y] = value

    def show_map_data(self):
        for i in range(self.h):
            for j in range(self.w):
                print(self.map_data[i][j], " ")
            print("")
