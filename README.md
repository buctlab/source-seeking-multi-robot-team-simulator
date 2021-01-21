# Source-Seeking Multi-robot Team Simulator

The python code is used in the manuscript Source-Seeking Multi-robot Team Simulator as Container of Nature-Inspired Metaheuristic Algorithms and Astar Algorithm.

The programming environment is:  `Python 3.8` or higher.

Required packages:

* pygame (Version 2.0.2)
* numpy (Version 1.19.4)
* pandas (Version 1.1.4)
* Pillow (Version 8.0.1)
* matplotlib (Version 3.3.3)
* tqdm (Version 4.54.0)

All above packages are easy to install by pip.



## How to use

The part of **quick start** is used to reproduce the source-seeking in the manuscript.

The part of  **More details** is a guide for customized source-seeking.

### Quick start

1. single source function

   * Run `main.py` in **SourceSeekingSimulation/main.py** 

2. muti-source function

   1.  Use the following parameters to modify the configuration in `Config.py`

      ```python
      func = MultiSourceFunction()
      NIM_data_file_path = os.path.join(project_root, "data/csv_file/ssa_MultiSourceFunction_8.csv")
      contour_img_path = os.path.join(project_root, "data/bg/contour/MultiSourceFunction.png")
      leakage_sources = 2
      iterations = 500
      ```

   2. Run `main.py` in **SourceSeekingSimulation/main.py** 

### More details

1. **Scene Construction**
   1. Modify scene size in `Config.py`
   2. Run `main.py` in SceneConstruction/main.py to construct your own scene.
   3. Save your scene.
2. **NIM**
   1. Set single source function (**NIM/benchmarks/single_source_function** ) or muti-source function (**NIM/benchmarks/multi_source_function** )
   2. Draw filled contours in **NIM/tests/PlotContour/contour.py**
   3. Choose suitable algorithm (take `S(a)sa` as an example)
   4. Modify config in `Config.py`
   5. Run `ssa_test.py` in **NIM/tests/ssa_test.py**

3. **Source Seeking Simulation**
   1. Set robot attributes in `Config.py`
   2. Run `main.py` in **SourceSeekingSimulation/main.py**
