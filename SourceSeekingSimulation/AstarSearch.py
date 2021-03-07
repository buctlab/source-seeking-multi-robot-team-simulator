import PIL
import numpy

from Config import Config


class AstarNode:
    def __init__(self, point, end_point, father=None):
        self.point = point
        self.end_point = end_point
        self.father = father
        if father is not None:
            self.gc = father.gc + self.get_gc()
            self.fc = 0
            self.hc = 0
        else:
            self.gc = 0
            self.fc = 0
            self.hc = 0

    # g value
    def get_gc(self):
        if abs(self.point[0] - self.father.point[0]) + abs(self.point[1] - self.father.point[1]) == 2:
            return 14
        else:
            return 10

    # h value
    def get_hc(self):
        return abs(self.point[0] - self.end_point[0]) + abs(self.point[1] - self.end_point[1])

    # set father
    def reset_father(self, father, new_gc):
        if father is not None:
            self.gc = new_gc
            self.fc = self.gc + self.hc
        self.father = father


class Astar:
    def __init__(self, pass_tag=0):
        self.open_list = dict()
        self.close_list = dict()
        self.map2d = None
        self.start_point = None
        self.end_point = None
        self.start_node = None
        self.end_node = None
        self.size1 = None
        self.size2 = None
        self.block_tag = pass_tag
        self.path = []
        self.closed_node = None

    def set_map_and_point(self, map2d, start_point, end_point, vertical, horizontal):
        self.map2d = map2d
        self.start_point = start_point
        self.end_point = end_point
        self.start_node = AstarNode(start_point, end_point)
        self.end_node = AstarNode(end_point, end_point)
        self.closed_node = AstarNode(start_point, end_point)
        self.size1 = vertical
        self.size2 = horizontal

    def reset_open_and_close_list(self):
        self.open_list.clear()
        self.close_list.clear()

    def find_path(self):
        self.open_list[self.start_point] = self.start_node
        node = self.start_node
        try:
            while not self.add_adjacent_int_open_list(node):
                node = self.find_min_fc_node()
        except Exception as e:
            print(e)
            # print(e)
            return False
        return True

    def find_min_fc_node(self):
        init_min = 99999
        init_point = self.start_point
        for point, node in self.open_list.items():
            if init_min > node.fc:
                init_min = node.fc
                init_point = point
        return self.open_list[init_point]

    def get_boundary(self, p, size):
        if size == 0:
            return p, p
        else:
            return p, min(len(self.map2d) - 1, p - 1 + size)

    def check_size(self, point):
        l1, r1 = self.get_boundary(point[0], self.size1)
        l2, r2 = self.get_boundary(point[1], self.size2)

        if r1 - l1 + 1 != self.size1:
            return False

        if r2 - l2 + 1 != self.size2:
            return False

        for i in range(l1, r1 + 1):
            for j in range(l2, r2 + 1):
                if self.map2d[i][j] == 1:
                    return False
        return True

    def check_boundary(self, point):
        return 0 <= point[0] < len(self.map2d) and 0 <= point[1] < len(self.map2d[-1])

    def check_point(self, point):
        return self.map2d[point[0]][point[1]] != 1

    def is_passable(self, point):
        if self.check_boundary(point) and self.check_point(point) and self.check_size(point):
            return True
        else:
            return False

    def add_adjacent_int_open_list(self, node: AstarNode):
        self.open_list.pop(node.point)
        self.close_list[node.point] = node

        adjacent_list = []
        for i in [0, -1, 1]:
            for j in [0, -1, 1]:
                if i == 0 and j == 0:
                    continue
                new_adjacent = (node.point[0] + i, node.point[1] + j)
                if self.is_passable(new_adjacent):
                    adjacent_list.append(AstarNode(new_adjacent, self.end_point, node))
        for adjacent in adjacent_list:
            if adjacent.point == self.end_point:
                gc = node.gc + adjacent.get_gc()
                self.end_node.reset_father(node, gc)
                return True
            # in close list
            if adjacent.point in self.close_list.keys():
                continue
            # not in open list
            if adjacent.point not in self.open_list.keys():
                self.open_list[adjacent.point] = adjacent
                current_point = adjacent.point
                if self.closed_node.get_hc() > adjacent.get_hc():
                    self.closed_node = adjacent
            # in open list
            else:
                exist_node = self.open_list[adjacent.point]
                if node.gc + exist_node.get_gc() < exist_node.get_gc():
                    exist_node.reset_father(node, node.gc + exist_node.get_gc())
        return False

    def get_ori_path(self, t_node):
        self.path.clear()
        node = t_node
        self.path.append(node.point)
        while node.father is not None:
            self.path.append(node.father.point)
            node = node.father
        return self.path.reverse()

    def astar_path(self, map2d, start_point, end_point, vertical, horizontal):
        '''
        get path from start to end
        :param map2d: scene data
        :param start_point: start position
        :param end_point: end position
        :param vertical: vertical size
        :param horizontal: horizontal size
        :return: path from start to end
        '''
        self.set_map_and_point(map2d, start_point, end_point, vertical, horizontal)
        if self.find_path():
            self.get_ori_path(self.end_node)
            self.reset_open_and_close_list()
            return self.path
        else:
            return []


class AstarSearch:
    def __init__(self, tag=0):
        self.astar = Astar(tag)

    def get_path(self, map2d, start_point, end_point, vertical, horizontal):
        '''
        get path from start to end
        :param map2d: scene data
        :param start_point: start position
        :param end_point: end position
        :param vertical: vertical size
        :param horizontal: horizontal size
        :return: path from start to end
        '''
        # print(start_point, end_point, vertical, horizontal)

        if start_point == end_point:
            return []
        else:
            return self.astar.astar_path(map2d, start_point, end_point, vertical, horizontal)


def check_occupation(use_map, h, w, size):
    for i in range(size[0]):
        for j in range(size[1]):
            if use_map[h + j][w + i] == 1:
                return False
    return True


def position_correction(use_map, h, w, size):
    w_min = max(0, w - size[0] + 1)
    h_min = max(0, h - size[1] + 1)
    print(w_min, h_min)
    print(list(range(h_min, h + 1)))
    print(list(range(w_min, w + 1)))
    available_position = []
    for i in range(h_min, h + 1):
        for j in range(w_min, w + 1):
            print(i, j)
            if check_occupation(use_map, i, j, size):
                available_position.append((i, j))
    return available_position


if __name__ == '__main__':
    a, b = 2, 1
    size = (a, b)

    with open(Config.default_saved_scene_path, 'r') as f:
        data = f.read()
    map_data = eval(data)
    print(len(map_data))
    print(map_data[67][146])
    astar = AstarSearch()
    d = position_correction(map_data, 67, 146, size)
    print(d)
    for item in d:
        path = astar.get_path(map_data, (195, 196), item, a, b)
        if path:
            break
    default_img = PIL.Image.open(Config.default_saved_scene_img_path)
    default_img.convert("RGB")
    matrix = numpy.array(default_img)
    # img = numpy.array(img)
    # matrix.flags.writeable = True
    # matrix.flags.writeable = True
    print(matrix)
    # if not path:
    for item in path:
        x, y = item
        for i in range(a):
            for j in range(b):
                if map_data[x + i][y + j] == 1:
                    matrix[y + j][x + i] = 100
                else:
                    matrix[y + j][x + i] = 150
    # else:
    #     print(matrix[146][67])
    #     matrix[146][67] = 100
    image = PIL.Image.fromarray(matrix)
    image.show()
