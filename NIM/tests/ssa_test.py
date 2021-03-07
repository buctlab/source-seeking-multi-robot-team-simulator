import os

from Config import Config
from NIM.algorithms import SalpSwarmAlgorithm
from NIM.algorithms.algorithm import logger

if __name__ == '__main__':
    with open(Config.default_saved_scene_path, 'r') as f:
        data = f.read()
    m2d = eval(data)
    seed = 1
    ssa = SalpSwarmAlgorithm(m2d, Config.rasterized_cell_size, func=Config.func, iterations=Config.iterations,
                             debug=True, k=Config.leakage_sources, population=Config.number_of_robots,
                             robot_size=Config.size, seed=seed)

    func_name = type(ssa.func).__name__
    best_sol, best_val = ssa.run()
    logger.info("best sol:{sol}, best val:{val}".format(sol=best_sol, val=best_val))
    ssa.iter_swarm_pos.to_csv(
        os.path.join(Config.project_root, "data/csv_file/ssa_" + func_name + "_" + str(seed) + ".csv"))
