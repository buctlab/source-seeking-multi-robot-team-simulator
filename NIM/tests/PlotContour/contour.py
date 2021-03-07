import inspect
import os

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from Config import Config
from NIM import benchmarks
from PIL import Image

classes = inspect.getmembers(benchmarks, inspect.isclass)
step = 0
ignore_benchmarks_name = ["Benchmark", "Eggholder", "Griewank", "Schwefel"]
unignore_benchmarks_name = ["SingleSourceFunction"]
# unignore_benchmarks_name = ["SingleSourceFunction", "MultiSourceFunction"]
for (benchmarks_name, benchmarks_class) in tqdm(classes):
    # if benchmarks_name in ignore_benchmarks_name:
    #     continue
    if benchmarks_name not in unignore_benchmarks_name:
        continue
    bc = benchmarks_class(dimension=3)
    if bc.upper[1] - bc.lower[1] >= 200 or bc.upper[0] - bc.lower[0] >= 200:
        step = 1
    elif 200 > bc.upper[1] - bc.lower[1] >= 50 or 200 > bc.upper[0] - bc.lower[0] >= 50:
        step = 0.1
    else:
        step = 0.1
    x = np.arange(bc.lower[0], bc.upper[0], step)
    y = np.arange(bc.lower[1], bc.upper[1], step)
    X, Y = np.meshgrid(x, y)
    Z = np.dstack((X, Y))
    Z = Z.reshape((Z.shape[0] * Z.shape[1], Z.shape[2]))
    Z = np.apply_along_axis(bc.eval, 1, Z)
    Z = Z.reshape((X.shape[0], X.shape[1]))
    Z = Z.astype(np.float64)

    Z[Z == 0] = 10 ** -20

    plt.figure(figsize=(5.4, 5.4), dpi=120)

    levels = [-4, -3, -2, -1, 1, 2, 3, 4]

    plt.contourf(X, Y, np.log(Z), cmap=plt.get_cmap('Pastel2'))

    axis = plt.axis()
    ax = plt.gca()
    ax.xaxis.set_ticks_position("top")
    ax.invert_yaxis()

    plt.scatter(bc.get_optimum()[0][0][0], bc.get_optimum()[0][0][1], marker='*', c="r")
    # plt.scatter(bc.get_optimum()[0][1][0], bc.get_optimum()[0][1][1], marker='*', c="r")

    name = benchmarks_name + ".png"
    plt.axis('off')

    plt.savefig("./out/" + name, bbox_inches='tight', pad_inches=0)
    plt.savefig(os.path.join(Config.project_root, "data/bg/contour", name), bbox_inches='tight', pad_inches=0)
    plt.clf()

    image = Image.open("./out/" + name)
    resized_image = image.resize((Config.contour_pixel, Config.contour_pixel), Image.ANTIALIAS)
    resized_image.save(os.path.join(Config.project_root, "data/bg/contour", name), quality=100)
