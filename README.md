# Installation

Required libraries: `pandas, scikit-learn, numpy`

Required tools: [jGetMove](https://github.com/jGetMove/jGetMove/)

You will also need a `directory_config.py` file with these global variables :

* `WORKING_DIR`: a directory with proper writing rights
* `JGETMOVE_DIR`: the directory where `jGetMove.jar` is located

Example:

```python
WORKING_DIR = "/home/me/wdir"
JGETMOVE_DIR = "/home/me/tools/jGetMove"
```

# How to use

Usage: `python main.py {start_date} {start_date} {end_date} {frequency} {DBSCAN_epsilon} {DBSCAN_min_t} {csv_file}`

Example call: `python main.py 2009-05-27 2009-08-27 2D 0.3 4 data.csv`

