import os

from Config import Config
from NIM.algorithms import WhaleOptimizationAlgorithm
from NIM.algorithms.algorithm import logger


if __name__ == '__main__':
    with open(Config.default_saved_scene_path, 'r') as f:
        data = f.read()
    m2d = eval(data)
    seed = 5

    woa = WhaleOptimizationAlgorithm(m2d, Config.rasterized_cell_size, func=Config.func, iterations=Config.iterations,
                                     debug=True, population=Config.number_of_robots, robot_size=Config.size, seed=seed,
                                     k=Config.leakage_sources)

    best_sol, best_val = woa.run()
    logger.info("best sol:{sol}, best val:{val}".format(sol=best_sol, val=best_val))

    func_name = type(woa.func).__name__
    woa.iter_swarm_pos.to_csv(
        os.path.join(Config.project_root, "data/csv_file/woa_MultiSourceFunction_" + str(seed) + ".csv"))
