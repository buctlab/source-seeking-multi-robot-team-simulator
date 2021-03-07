from NIM.algorithms.algorithm import Algorithm
from NIM.algorithms.ant_lion_optimizer import AntLionOptimizer
from NIM.algorithms.bat_algorithm import BatAlgorithm
from NIM.algorithms.cuckoo_search import CuckooSearch
from NIM.algorithms.differential_evolution import DifferentialEvolution
from NIM.algorithms.dispersive_flies_optimisation import DispersiveFliesOptimisation
from NIM.algorithms.firefly_algorithm import FireflyAlgorithm
from NIM.algorithms.flower_pollination_algorithm import FlowerPollinationAlgorithm
from NIM.algorithms.fruitfly_optimization_algorithm import FruitFly
from NIM.algorithms.genetic_algorithm import GeneticAlgorithm
from NIM.algorithms.grey_wolf_optimizer import GreyWolfOptimizer
from NIM.algorithms.krill_herd import KrillHerdBase, KrillHerd
from NIM.algorithms.moth_flame_optimization import MothFlameOptimization
from NIM.algorithms.particle_swarm_optimization import ParticleSwarmOptimization
from NIM.algorithms.salp_swarm_algorithm import SalpSwarmAlgorithm
from NIM.algorithms.squirrel_search_algorithm import SquirrelSearchAlgorithm
from NIM.algorithms.water_wave_optimization import WaterWaveOptimization
from NIM.algorithms.whale_optimization_algorithm import WhaleOptimizationAlgorithm
# from NIM.algorithms.random_calculation import RandomCalculation
from NIM.algorithms.rooted_tree_optimization import RootedTreeOptimization
from NIM.algorithms.black_widow_optimization_algorithm import BlackWidowOptimizationAlgorithm
from NIM.algorithms.sailfish_optimizer import SailfishOptimizer

__all__ = [
    'Abbreviation',
    'Algorithm',
    'AntLionOptimizer',
    'BatAlgorithm',
    'CuckooSearch',
    'DifferentialEvolution',
    'DispersiveFliesOptimisation',
    'FireflyAlgorithm',
    'FlowerPollinationAlgorithm',
    'FruitFly',
    'GeneticAlgorithm',
    'GreyWolfOptimizer',
    'KrillHerd',
    'MothFlameOptimization',
    'ParticleSwarmOptimization',
    'SalpSwarmAlgorithm',
    'SquirrelSearchAlgorithm',
    'WaterWaveOptimization',
    'WhaleOptimizationAlgorithm',
    # 'RandomCalculation',
    'RootedTreeOptimization',
    'BlackWidowOptimizationAlgorithm',
    'SailfishOptimizer'
]

Abbreviation = {
    'AntLionOptimizer': 'ALO',
    'BatAlgorithm': 'BA',
    'CuckooSearch': 'CS',
    'DifferentialEvolution': 'DE',
    'DispersiveFliesOptimisation': 'DFO',
    'FireflyAlgorithm': 'FA',
    'FlowerPollinationAlgorithm': 'FPA',
    'FruitFly': 'FOA',
    'GeneticAlgorithm': 'GA',
    'GreyWolfOptimizer': 'GWO',
    'KrillHerd': 'KH',
    'MothFlameOptimization': 'MFO',
    'ParticleSwarmOptimization': 'PSO',
    'SalpSwarmAlgorithm': 'S(a)SA',
    'SquirrelSearchAlgorithm': 'S(q)SA',
    'WaterWaveOptimization': 'WWO',
    'WhaleOptimizationAlgorithm': 'WOA',
    "RootedTreeOptimization": 'RTO',
    "BlackWidowOptimizationAlgorithm": "BWOA",
    "SailfishOptimizer": "SFO"
}
